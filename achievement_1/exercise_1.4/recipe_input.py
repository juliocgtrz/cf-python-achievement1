# Import pickle module to work with binary files
import pickle

# Function to take user input for components of recipes
def take_recipe():
    name = str(input("Enter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = list(input("Enter the list of ingredients, separate with a comma: ").split(", "))
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": ""
    }

    # Calculates recipe difficulty
    def calc_difficulty():
        if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
            recipe["difficulty"] = "Easy"
        elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
            recipe["difficulty"] = "Medium"
        elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
            recipe["difficulty"] = "Intermediate"
        elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
            recipe["difficulty"] = "Hard"

    calc_difficulty()

    return recipe

# Attempt to open a user-defined binary file in read mode
file_name = input("Enter a file name to read: ")

try:
    file = open(file.name, "rb")
    data = pickle.load(file)
    print("File loaded")

# If user-defined file is not found, this creates a new one with a data dictionary
except FileNotFoundError:
    print("No such file exists. Creating new file..")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }

# If a different error occurs, this performs same operations as previous except block
except:
    print("Oops, we've stumbled upon an unexpected error")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }

# Closes the file stream
else:
    file.close()

# Extract values from the data dictionary
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

# User prompt
n = int(input("How many recipes would you like to enter? "))

# Iterate through number of entered recipes
for i in range(n):
    recipe = take_recipe()

    # Check whether an ingredient should be added to an ingredient list
    for ingredient in recipe["ingredients"]:
        if not ingredient in all_ingredients:
            all_ingredients.append(ingredient)

    recipes_list.append(recipe)
    print("Recipe added")

# Gather the updated data into a new dictionary
data = {
    "recipes_list": recipes_list,
    "all_ingredients": all_ingredients
}

# Open the user-defined file name and write to it
updated_file = open(file_name, "wb")
pickle.dump(data, updated_file)
updated_file.close()
print("File has been updated")
