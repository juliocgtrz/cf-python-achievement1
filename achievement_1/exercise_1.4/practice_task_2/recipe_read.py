import pickle

with open('recipe_binary.bin', 'rb') as my_file:
    recipe = pickle.load(my_file)

print("---Recipe Details---")
print("Name: " + recipe["ingredient_name"])
print("Ingredients: " + ", ".join(recipe["ingredients"]))
print("Cooking Time: " + str(recipe["cooking_time"]))
print("Difficutly: " + recipe["difficulty"])
