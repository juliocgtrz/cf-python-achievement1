# Connect SQL and Python
import mysql.connector

# Initialize connection object to MySQL server
conn = mysql.connector.connect(
    host = "localhost",
    user = "cf-python",
    passwd = "password"
)

# Perform operations on the database using SQL queries
cursor = conn.cursor()

# Create the 'task_database' with statement to avoid using multiple databases with same name
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

# Access the database
cursor.execute("USE task_database")

# Create 'Recipes' table with statement to avoid using table with the same name
cursor.execute("""CREATE TABLE IF NOT EXISTS Recipes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)
)""")

# Determine recipe difficulty
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = "Hard"
    return difficulty

# MAIN MENU
# Define the functions for the main menu
def main_menu():
    # Function for creating a new recipe
    def create_recipe(conn, cursor):
        # Empty list for the recipe ingredients
        ingredients_list = []

        # User input for recipe attributes
        name = str(input("\nEnter the name of the recipe: "))
        cooking_time = int(input("Enter the cooking time in minutes: "))
        ingredients = input("Enter the list of ingredients, separate with a comma: ")

        # Append user provided ingredients to list then convert list to joined string
        ingredients_list.append(ingredients)
        ingredients_str = ", ".join(ingredients_list)
        difficulty = calc_difficulty(cooking_time, ingredients_list)

        # Build SQL query string
        sql_query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
        sql_values = (name, ingredients_str, cooking_time, difficulty)
        cursor.execute(sql_query, sql_values)
        conn.commit()
        print("\nRecipe successfully created.\n")

    # Function to search for a recipe
    def search_recipe(conn, cursor):
        # Empty list for all ingredients
        all_ingredients = []

        # Select values in 'ingredients' column from 'Recipes' table
        cursor.execute("SELECT ingredients FROM Recipes")
        results = cursor.fetchall()

        # Get ingredients from 'ingredients' column and add to all_ingredients
        for ingredients_list in results:
            for ingredient in ingredients_list:
                split_ingredients = ingredient.split(", ")
                all_ingredients.extend(split_ingredients)

        # Remove duplicate ingredients from all_ingredients
        all_ingredients = list(dict.fromkeys(all_ingredients))
        numbered_ingredients = list(enumerate(all_ingredients))

        # Number and sort each ingredient from list and prints
        print("\nIngredients list:")
        print("-----------------\n")

        for index, ingredient in enumerate(numbered_ingredients):
            print(str(ingredient[0] + 1) + ". " + ingredient[1])

        # Search for user-defined ingredient id
        try:
            n = int(input("\nEnter the number of an ingredient to search: "))
            true_index = n - 1

            # Store the user-defined ingredient
            ingredient_searched = numbered_ingredients[true_index][1]
            print(f"\nSearching for recipes with {ingredient_searched}..")

        # If user enters anything but an integer, error informing user
        except ValueError:
            print("\nInvalid entry. Enter a number only")

        # Print all recipes that contain the user-defined ingredient
        else:
            print(f"\nRecipes containing {ingredient_searched}:")
            print("--------------------------------------------")

            # Selects 'ingredients' from 'Recipes' table
            cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s", ("%" + ingredient_searched + "%",))
            recipes_searched = cursor.fetchall()

            # Print each recipe containing the user-defined ingredient
            if recipes_searched:
                for recipe in recipes_searched:
                    print("\nID: ", recipe[0])
                    print("Name: ", recipe[1])
                    print("Ingredients: ", recipe[2])
                    print("Cooking Time (minutes): ", recipe[3])
                    print("Difficulty: ", recipe[4])
                    print()
            else:
                print(f"No recipes found with {ingredient_searched}.\n")

    # Function to update an existing recipe
    def update_recipe(conn, cursor):
        # Select all recipes from 'Recipes' table
        cursor.execute("SELECT * FROM Recipes")
        recipes_selected = cursor.fetchall()
        print("\nRecipes:")
        print("--------\n")

        # List all recipes
        for recipe in recipes_selected:
            # Split the ingredients list with commas
            ingredients_list = recipe[2].split(", ")
            ingredients_str = ", ".join(ingredients_list)
            print("ID: ", recipe[0])
            print("Name: ", recipe[1])
            print("Ingredients: ", ingredients_str)
            print("Cooking Time (minutes): ", recipe[3])
            print("Difficulty: ", recipe[4])

        # Store the user-defined recipe and attribute to update
        id_to_update = int(input("\nEnter the ID of the recipe to update: "))
        column_to_update = str(input("Enter one of the following to update: \nname \ncooking_time \ningredients\n\n"))
        new_value = input("\nEnter the new value: ")

        # Determine column to update and update value with new_value
        if column_to_update == "name":
            cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_value, id_to_update))
            print(f"Recipe name updated to {new_value}\n")
        elif column_to_update == "cooking_time":
            cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_value, id_to_update))
            print(f"Cooking Time updated to {new_value}\n")

            # Reselect recipe to use new value
            cursor.execute("SELECT * FROM Recipes WHERE id = %s", (id_to_update,))
            working_recipe = cursor.fetchall()
            ingredients = tuple(working_recipe[0][2].split(", "))
            cooking_time = working_recipe[0][3]

            # Recalculate difficulty based on new ingredients and cooking time
            updated_difficulty = calc_difficulty(cooking_time, ingredients)
            cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (updated_difficulty, id_to_update))
            print(f"Difficulty updated to {updated_difficulty}\n")

        elif column_to_update == "ingredients":
            cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (new_value, id_to_update))
            print(f"Ingredients updated to {new_value}\n")

            # Reselect recipe to use new value
            cursor.execute("SELECT * FROM Recipes WHERE id = %s", (id_to_update,))
            working_recipe = cursor.fetchall()
            ingredients = tuple(working_recipe[0][2].split(", "))
            cooking_time = working_recipe[0][3]

            # Recalculate difficulty based on new ingredients and cooking time
            updated_difficulty = calc_difficulty(cooking_time, ingredients)
            cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (updated_difficulty, id_to_update))
            print(f"Difficulty updated to {updated_difficulty}\n")

        conn.commit()

    # Function to delete a recipe
    def delete_recipe(conn, cursor):
        cursor.execute("SELECT * FROM Recipes")
        recipes_selected = cursor.fetchall()
        print("\nRecipes:")
        print("--------\n")

        # List all recipes
        for recipe in recipes_selected:
            # Split ingredients list with commas
            ingredients_list = recipe[2].split(", ")
            ingredients_str = ", ".join(ingredients_list)
            print("ID: ", recipe[0])
            print("Name: ", recipe[1])
            print("Ingredients: ", ingredients_str)
            print("Cooking Time (minutes): ", recipe[3])
            print("Difficulty: ", recipe[4])
            print()

        id_to_delete = input("\nEnter the ID of a recipe to delete: ")
        cursor.execute("DELETE FROM Recipes WHERE id = %s", (id_to_delete,))
        print("\nRecipe successfully deleted\n")
        conn.commit()

    # for Loop for the main menu that stops when the user quits
    choice = ""
    while(choice != "quit"):
        print("What would you like to do? Pick a number!")
        print("1. Create a Recipe")
        print("2. Search for a Recipe")
        print("3. Update a Recipe")
        print("4. Delete a Recipe")
        print("Type 'quit' to exit the program\n")
        choice = input("Select an option: ")

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        else:
            conn.commit()
            conn.close()

# Call main_menu()
main_menu()
