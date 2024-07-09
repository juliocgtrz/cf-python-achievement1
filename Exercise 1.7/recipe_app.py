# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

# Connect SQLAlchemy to task_database
engine = create_engine("mysql+pymysql://cf-python:password@localhost/task_database")

# Create a session by binding engine and initialize session object
Session = sessionmaker(bind=engine)
session = Session()

# RECIPE MODEL
# Store declarative base class
Base = declarative_base()


# Define Recipe model
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(225))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Define string representation to identify objects in terminal
    def __repr__(self):
        return f"<Recipe ID: {self.id} - {self.name} ({self.difficulty})>"

    # Define string representation for printing
    def __str__(self):
        ingredients_list = self.ingredients.split(", ")
        ingredients_str = ", ".join(ingredients_list)

        return (
            f"Recipe ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Ingredients: {ingredients_str}\n"
            f"Cooking Time (minutes): {self.cooking_time}\n"
            f"Difficulty: {self.difficulty}\n"
        )

    # Determine recipe difficulty
    def calc_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "Hard"
        return self.difficulty

    # Retrieve ingredients string as a list
    def return_ingredients_as_list(self):
        if self.ingredients == "":
            return []
        else:
            return self.ingredients.split(", ")


# Create the table from the database
Base.metadata.create_all(engine)


# MAIN OPERATIONS
# Define create_recipe()
def create_recipe():
    # Take user input for recipe name and checks if valid input
    while True:
        name = input("Enter the name of the recipe: ").strip()

        if len(name) > 50:
            print("Name must be 50 characters or less")
            continue

        if not name.replace(" ", "").isalnum():
            print("Name must only contain alphanumeric characters and spaces")
            continue

        break

    # Take user input for cooking_time and checks if valid input
    while True:
        cooking_time = input("Enter the cooking time in minutes: ").strip()

        if not cooking_time.isnumeric():
            print("Cooking time must be a number")
            continue

        cooking_time = int(cooking_time)

        break

    # Take user input for ingredients and check if valid input
    ingredients = []

    while True:
        try:
            n = int(input("How many ingredients would you like to enter? ").strip())

            if n <= 0:
                print("You must enter at least one ingredient")
                continue

            break

        except ValueError:
            print("Enter a valid number")

    for i in range(n):
        while True:
            ingredient = input(f"Enter ingredient {i + 1}: ").strip()

            if not all(char.isalpha() or char.isspace() for char in ingredient):
                print("Ingredient must only contain alphabetical characters and spaces")
                continue

            ingredients.append(ingredient)

            break

    ingredients_str = ", ".join(ingredients)

    # Create recipe object
    recipe_entry = Recipe(
        name=name, cooking_time=cooking_time, ingredients=ingredients_str, difficulty="",
    )

    # Calculate recipe difficulty
    recipe_entry.difficulty = recipe_entry.calc_difficulty()

    # Add recipe to the session and commit changes
    session.add(recipe_entry)
    session.commit()

    print("\nRecipe successfully added")


# Define view_all_recipes()
def view_all_recipes():
    # Get all recipes from database and store in recipes object
    recipes = session.query(Recipe).all()

    if not recipes:
        print("There are no recipes in the database")
        return None

    # Print each recipe via the __str__() method
    for recipe in recipes:
        print(recipe)


# Define search_by_ingredients()
def search_by_ingredients():
    # Check if the table has any entries
    if session.query(Recipe).count() == 0:
        print("There are no entries in this table")
        return None

    # Get values from ingredients column
    results = session.query(Recipe.ingredients).all()

    # Initialize empty list for all_ingredients
    all_ingredients = []

    # Add each ingredient from results to all_ingredients if doesn't already exist
    for result in results:
        ingredients_list = result[0].split(", ")

        for ingredient in ingredients_list:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    # Display numbered ingredients
    print("\nAvailable Ingredients:")
    print("----------------------\n")

    for i, ingredient in enumerate(all_ingredients, start=1):
        print(f"{i}. {ingredient}")

    # Take user input to select ingredients by number
    selected_numbers = input(
        "Select ingredients by their numbers, separated by spaces: "
    ).split()

    try:
        true_index = [int(num) - 1 for num in selected_numbers]

        if any(i < 0 or i >= len(all_ingredients) for i in true_index):
            raise ValueError

    except ValueError:
        print("Invalid input")
        return None

    # Create list of ingredients to search
    search_ingredients = [all_ingredients[i] for i in true_index]

    # Initialize list of conditions and use a search string to add like terms to it
    conditions = []

    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))

    # Retrieve recipes matching specified conditions
    recipes = session.query(Recipe).filter(*conditions).all()

    # Display recipes if found
    if recipes:
        for recipe in recipes:
            print()
            print(recipe)
    else:
        print("No recipes found with the selected ingredients")


# Define edit_recipe()
def edit_recipe():
    # Check if there are any recipes in the database
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database")
        return None

    # Get ID and name of each recipe
    results = session.query(Recipe.id, Recipe.name).all()

    # Display available recipes
    print("\nAvailable Recipes:")
    print("------------------\n")

    for recipe_id, recipe_name in results:
        print(f"{recipe_id}. {recipe_name}")

    # Take user input to select recipe by ID
    try:
        selected_id = int(input("\nEnter the ID of the recipe to edit: ").strip())

    except ValueError:
        print("Invalid input")
        return None

    # Get corresponding recipe by ID
    recipe_to_edit = session.query(Recipe).filter_by(id=selected_id).first()

    if not recipe_to_edit:
        print("The selected ID does not exist")
        return None

    # Display recipe details
    print("\nSelected recipe:")
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Cooking Time (minutes): {recipe_to_edit.cooking_time}")
    print(f"3. Ingredients: {recipe_to_edit.ingredients}")

    # Take user input to select an attribute to edit
    try:
        attribute_choice = int(
            input("\nEnter the number of the attribute to edit: ").strip()
        )

        if attribute_choice not in [1, 2, 3]:
            raise ValueError

    except ValueError:
        print("Invalid input")
        return None

    # Edit the user selected attribute
    # NAME
    if attribute_choice == 1:
        new_name = input("\nEnter new recipe name: ").strip()

        if len(new_name) > 50:
            print("Name must be 50 characters or less")
            return None

        if not new_name.replace(" ", "").isalnum():
            print("Name should only contain alphanumeric characters")
            return None

        recipe_to_edit.name = new_name

    # COOKING TIME
    elif attribute_choice == 2:
        try:
            new_cooking_time = int(
                input("\nEnter new cooking time (minutes): ").strip()
            )

        except ValueError:
            print("Cooking time must be a number")
            return None

        recipe_to_edit.cooking_time = new_cooking_time

    # INGREDIENTS
    elif attribute_choice == 3:
        new_ingredients = input(
            "\nEnter new ingredients, separate with a commas: "
        ).strip()

        ingredients_list = [
            ingredient.strip() for ingredient in new_ingredients.split(", ")
        ]

        if not all(
            all(char.isalpha() or char.isspace() for char in ingredient)
            for ingredient in ingredients_list
        ):
            print("Each ingredient must only contain alphabetical characters")
            return None

        recipe_to_edit.ingredients = ", ".join(ingredients_list)

    # Recalculate recipe difficulty
    recipe_to_edit.difficulty = recipe_to_edit.calc_difficulty()

    # Commit changes to database
    session.commit()

    print("\nRecipe successfully updated")


# Define delete_recipe()
def delete_recipe():
    # Check if there are any recipes in the database
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database")
        return None

    # Get ID and name of each recipe
    results = session.query(Recipe.id, Recipe.name).all()

    # Display available recipes
    print("\nAvailable Recipes:")
    print("------------------\n")

    for recipe_id, recipe_name in results:
        print(f"{recipe_id}. {recipe_name}")

    # Take user input to select recipe by ID
    try:
        selected_id = int(input("\nEnter the ID of the recipe to delete: ").strip())

    except ValueError:
        print("Invalid input")
        return None

    # Get corresponding recipe by ID
    recipe_to_delete = session.query(Recipe).filter_by(id=selected_id).first()

    if not recipe_to_delete:
        print("The selected ID does not exist")
        return None

    # Display selected recipe name
    print(f"\nRecipe to delete: {recipe_to_delete.name}")

    # Take user input to confirm recipe deletion
    confirmation = input(
        "\nAre you sure you want to delete this recipe? (Y/N)\n"
    ).strip()

    if confirmation == "Y":
        session.delete(recipe_to_delete)
        session.commit()

        print("\nRecipe successfully deleted")
    else:
        print("\nCancelling deletion..")


# MAIN MENU
# Define main_menu()
def main_menu():
    while True:
        # Display menu options
        print("\nRecipes Main Menu")
        print("-----------------\n")
        print("1. Create new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit recipe")
        print("5. Delete recipe")
        print("Type 'quit' to exit the app\n")

        # Take user input for selecting a menu option
        choice = input("Select an option: ").strip()

        # Execute corresponding function based on user input
        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "quit":
            print("\nExiting the app..")
            session.close()
            engine.dispose()
            break
        else:
            print("invalid input")


# MAIN CODE
main_menu()
