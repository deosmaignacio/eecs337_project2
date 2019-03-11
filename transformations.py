import tagdata, sys, parseurl

def main():
	url = input("Enter allRecipes.com URL:" + '\n')
	recipeList = parseurl.processhtml(url)

	ingredients = tagdata.tag_ingredients(recipeList)
	print('\n')
	for ingredient in ingredients.keys():
		print("Ingredient Name: " + ingredient)
		ingredientInfo = ingredients[ingredient].keys()
		if "quantity" in ingredientInfo:
			print("Quantity: " + str(ingredients[ingredient]["quantity"]))
		if "measurement" in ingredientInfo:
			print("Measurement: " + str(ingredients[ingredient]["measurement"]))
		if "descriptor" in ingredientInfo:
			print("Descriptor: " + str(ingredients[ingredient]["descriptor"]))
		if "preparation" in ingredientInfo:
			print("Preparation: " + str(ingredients[ingredient]["preparation"]))
		print('\n')

	tools = tagdata.find_tools(recipeList)
	print("Tools: ")
	for tool in tools:
		print(tool)
	print('\n')

	methods = tagdata.get_cooking_methods(recipeList) # function not working properly
	print("Methods: ")
	for method in methods:
		print(method)

	steps = tagdata.parse_steps(ingredients, tools, methods, recipeList)
	return

def toVegetarian():
	return

def fromVegetarian():
	return

def toHealthy():
	return

def fromHealthy():
	return

def toMexicanCuisine(): # or other if we want other style
	return

### Optionals ###
def toAsianCuisine():
	return

def DIY():
	return

def cookingMethod(): # i.e. from bake to stir fry
	return

if __name__ == '__main__':
	main()
