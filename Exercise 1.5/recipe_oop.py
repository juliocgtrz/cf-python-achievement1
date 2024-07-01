# Define Recipe class
class Recipe:
    # Initialize the data attributes
    def __init__(self, name, cooking_time):
        self.name = name
        self.ingredients = []
        self.cooking_time = cooking_time
        self.difficulty = None
    
    # NAME
    # Get recipe name
    def get_name(self):
        return self.name

    # Set recipe name
    def set_name(self, name):
        self.name = name

    # INGREDIENTS
    # Set a class variable to store all ingredients across all recipes
    all_ingredients = set()

    # Get the ingredients list
    def get_ingredients(self):
        return self.ingredients

    # Add ingredients to a recipe
    def add_ingredients(self, *ingredients):
        for ingredient in ingredients:
            self.ingredients.append(ingredient)

        # Update list of all ingredients
        self.update_all_ingredients()

    # Search for an ingredient
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    # Update the list of all ingredients when a new ingredient is added
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            Recipe.all_ingredients.add(ingredient)

    # COOKING TIME
    # Get cooking time for recipe
    def get_cooking_time(self):
        return self.cooking_time

    # Set cooking time for recipe
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    # DIFFICULTY
    # Determine recipe difficulty
    def calc_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >=4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "Hard"

    # Get a recipe's difficulty
    def get_difficulty(self):
        if not self.difficulty:
            self.calc_difficulty()
        return self.difficulty

    # STRING REPRESENTATION
    def __str__(self):
        return f"Recipe: {self.name}\nIngredients: {', '.join(self.ingredients)}\nCooking Time (minutes): {self.cooking_time}\nDifficulty: {self.get_difficulty()}\n"

# Search for a recipe containing a specific ingredient
def recipe_search(data, ingredient):
    for recipe in data:
        if recipe.search_ingredient(ingredient):
            print(recipe)

# Initialize Tea object
tea = Recipe("Tea", 5)
tea.add_ingredients("Tea leaves", "Sugar", "Water")
print(tea)

# Initialize Coffee object
coffee = Recipe("Coffee", 5)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
print(coffee)

# Initialize Cake object
cake = Recipe("Cake", 50)
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
print(cake)

# Initialize Banana Smoothie object
banana_smoothie = Recipe("Banana Smoothie", 5)
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
print(banana_smoothie)

# Initialize recipe list
recipes_list = [tea, coffee, cake, banana_smoothie]

# Use recipe_search() to find ingredients in recipes_list
print("\nRecipes with Water:")
print("---------------------")
recipe_search(recipes_list, "Water")

print("\nRecipes with Sugar:")
print("---------------------")
recipe_search(recipes_list, "Sugar")

print("\nRecipes with Bananas:")
print("-----------------------")
recipe_search(recipes_list, "Bananas")
