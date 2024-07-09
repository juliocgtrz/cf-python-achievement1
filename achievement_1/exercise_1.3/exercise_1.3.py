# Empty lists for recipes and ingredients
recipes_list = []
ingredients_list = []

# Function to take user input for components of recipes
def take_recipe():
    name = str(input("Enter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = list(input("Enter the list of ingredients, separate with a comma: ").split(", "))
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }

    return recipe

# User prompt
n = int(input("How many recipes would you like to enter? "))

# Iterate through number of entered recipes
for i in range(n):
    recipe = take_recipe()

    # Check whether an ingredient should be added to an ingredient list
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)

# Iterate through recipes_list to determine difficulty of recipe
for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Hard"

# Iterate through recipes_list to display recipe information
for recipe in recipes_list:
    print("Recipe: ", recipe["name"])
    print("Cooking Time (minutes): ", recipe["cooking_time"])
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty: ", recipe["difficulty"])

# Display all ingredients from all recipes in alphabetical order
def all_ingredients():
    print("Ingredients available across all recipes")
    print("________________________________________")
    ingredients_list.sort()
    for ingredient in ingredients_list:
        print(ingredient)

all_ingredients()