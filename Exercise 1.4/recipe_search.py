# Import pickle module to work with binary files
import pickle

# Function that takes in a recipe as an argument and prints all of its attributes
def display_recipe(recipe):
    print("Recipe: ", recipe["name"])
    print("Cooking Time (minutes): ", recipe["cooking_time"])
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty: ", recipe["difficulty"])

# Function that searches for an ingredient in the given data
def search_ingredient(data):
    all_ingredients = enumerate(data["all_ingredients"])
    numbered_ingredients = list(all_ingredients)

    # Displays each ingredient with a number
    print("Ingredients available across all recipes")
    print("----------------------------------------")
    for ingredient in numbered_ingredients:
        print(ingredient[0], ingredient[1])

    # Attempts to search for user-defined ingredient number
    try:
        n = int(input("Enter the number of an ingredient to search: "))

        # Stores the user-defined ingredient
        ingredient_searched = numbered_ingredients[n][1]
        print("Searching for recipes with that ingredient..")

    # If user enters anything other than an integer, error informing user
    except ValueError:
        print("Invalid input. Entry must be a number.")

    # Prints every recipe that contains the specified ingredient
    else:
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["ingredients"]:
                display_recipe(recipe)

# Attempts to load the user-defined file name
file_name = input("Enter the file name that contains the recipe data: ")

try:
    file = open(file_name, "rb")
    data = pickle.load(file)
    print("File loaded")

# If user-defined file name is not found, error informing the user
except FileNotFoundError:
    print("No such file exists")

# Closes the file stream and initializes search_ingredient()
else:
    file.close()
    search_ingredient(data)
    