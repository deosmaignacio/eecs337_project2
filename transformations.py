import tagdata, sys, parseurl, difflib

originalDish = ""
originalIngredients = {}
originalSteps = {}


def convertMeasurement(measurement):
	measurement = measurement.lower()
	if measurement == "pound":
		return "lb"
	elif measurement == "pounds":
		return "lbs"
	elif measurement == "kilogram":
		return "kg"
	elif measurement == "kilograms":
		return "kgs"
	elif measurement in ["ounces", "ounce"]:
		return "oz"
	else:
		return measurement

def determineCookingMethod(methods):
	if len(methods) > 0:
		knownMethods = ["grill", "pan-fry", "pan fry", "deep-fry", "deep fry", "saute", "sauté", "boil", "roast", "bake", "sear", "poach", "simmer", "broil", "steam", "blanch", "braise", "stew"]
		for method in methods:
			if method in knownMethods:
				return method
		matches = []
		for method in methods:
			currMatches = difflib.get_close_matches(method, knownMethods)
			if len(currMatches) > 0:
				matches.append(currMatches[0])

		if len(matches) > 0:
			print("matches: " + str(matches))
			return max(set(matches), key = matches.count)
		else:
			return methods[0]
	else:
		return "grill"

def extractDishName(url):
	urlSplit = url.split('/')
	dishNameUnprocessed = urlSplit[urlSplit.index('recipe') + 2]
	dishNameSplit = dishNameUnprocessed.split('-')
	dishName = ""
	for dishWord in dishNameSplit:
		dishName += dishWord.lower().capitalize() + " "
	return dishName



def originalRecipe(url):
	global originalDish
	global originalIngredients
	global originalSteps

	recipeList = parseurl.processhtml(url)
	originalDish = extractDishName(url)
	print(originalDish)

	ingredients = tagdata.tag_ingredients(recipeList)
	originalIngredients = ingredients
	print("originalIngredients: " + str(originalIngredients))
	tools = tagdata.find_tools(recipeList)
	methods = tagdata.get_cooking_methods(recipeList) # function not working properly
	steps = tagdata.parse_steps(ingredients, tools, methods, recipeList)
	originalSteps = steps

	print('\n')
	print("Ingredients: ")
	for ingredient in ingredients:
		quantity = int(ingredients[ingredient]['quantity'])
		measurement = ingredients[ingredient]['measurement']
		measurement = convertMeasurement(measurement)
		descriptor = ingredients[ingredient]['descriptor']
		if quantity == 0:
			print(str(measurement) + " " + ingredient + " " + str(descriptor))
		else:
			print(str(quantity).strip() + " " + str(measurement).strip() + " " + ingredient + " " + str(descriptor).strip())

	print('\n')
	print("Tools: ")
	for tool in tools:
		print(tool)
	print('\n')

	print("Main cooking method: " + determineCookingMethod(methods))

	numberOfSteps = len(steps.keys())
	print("Steps: ")
	print(steps)

def main():
	url = input("Enter allRecipes.com URL:" + '\n')
	print("--------------------------------")
	originalRecipe(url)
	print("--------------------------------")
	while True:
		transformation = int(input("Select one: " + '\n' + "1: To Vegetarian" + '\n' + "2: From Vegetarian" + '\n' + "3: To Healthy" + '\n' + "4: From Healthy" + '\n'))
		if transformation == 1:
			toVegetarian()
		elif transformation == 2:
			fromVegetarian()
		elif transformation == 3:
			toHealthy()
		elif transformation == 4:
			fromHealthy()



	return

def toVegetarian():
	return

def fromVegetarian():
	return

def toHealthy():
	global originalIngredients
	healthyRecipe = originalIngredients

	unhealthyReplacements = {'burger': 'turkey burger', 'rice': 'brown rice', 'noodles': 'zoocchini noodles', 'salt': 'iodized salt', 'pancetta': 'turkey ham', 'french fries': 'zucchini fries', 'fries': 'zucchini fries', 'pancake': 'banana pancakes', 'beef': 'turkey burger', 'ketchup': 'tomato sauce'}
	# replace cheeses with feta cheese (not all of them... doesn't make sense to replace parmesan in a pasta w/ feta cheese for instance)
	cheeseTypes = ['mozzarella', 'parmigiano-reggiano', 'parmigiano', 'parmigiano reggiano', 'goat', 'cheddar', 'american', 'monterey', 'jack', 'monterey jack', 'provolone', 'cheddar', 'brie', 'swiss', 'manchego']
	# replace all breads with Whole wheat Bread
	breadTypes = ['bread', 'white', 'multigrain', 'cornbread', 'ciabatta', 'naan', 'brioche', 'brown', 'focaccia', 'bagel', 'pita', 'flatbread', 'breadsticks']
	print("original Ingredients: " + str(originalIngredients))
	for originalIngredient in originalIngredients:
		ingredient = originalIngredient.replace(',', '')
		ingredientWords = ingredient.split()
		for unhealthyFood in unhealthyReplacements.keys():
			replacement = False
			if replacement:
				break
			for ingredientWord in ingredientWords:
				if replacement:
					break
				if ingredientWord in unhealthyFood:
					ingredientInfo = originalIngredients[originalIngredient]
					del healthyRecipe[ingredient]
					healthyRecipe[unhealthyReplacements[unhealthyFood]] = ingredientInfo
					replacement = True
					break
				elif ingredient in cheeseTypes:
					del healthyRecipe[ingredient]
					healthyRecipe[unhealthyReplacements[ingredient]] = 'goat cheese'
					replacement = True
					break
				elif ingredient in breadTypes:
					del healthyRecipe[ingredient]
					healthyRecipe[unhealthyReplacements[ingredient]] = 'whole wheat bread'
					replacement = True
					break

	print("--------------------------------")
	print("Healthy " + originalDish)
	for ingredient in healthyRecipe:
		quantity = int(healthyRecipe[ingredient]['quantity'])
		measurement = healthyRecipe[ingredient]['measurement']
		measurement = convertMeasurement(measurement)
		descriptor = healthyRecipe[ingredient]['descriptor']
		if quantity == 0:
			print(str(measurement) + " " + ingredient + " " + str(descriptor))
		else:
			print(str(quantity).strip() + " " + str(measurement).strip() + " " + ingredient + " " + str(descriptor).strip())
	print("--------------------------------")
	return

def fromHealthy():
	return

def toMexicanCuisine(): # or other style
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
