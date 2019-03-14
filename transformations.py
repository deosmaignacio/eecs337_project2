import tagdata, sys, parseurl, difflib

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
		matches = difflib.get_close_matches()
		if len(matches) > 0:
			return max(set(matches), key = matches.count)
		else:
			return methods[0]
	else:
		return "grill"

def main():
	url = input("Enter allRecipes.com URL:" + '\n')
	recipeList = parseurl.processhtml(url)

	ingredients = tagdata.tag_ingredients(recipeList)
	tools = tagdata.find_tools(recipeList)
	methods = tagdata.get_cooking_methods(recipeList) # function not working properly
	steps = tagdata.parse_steps(ingredients, tools, methods, recipeList)

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
	# for stepNumber in range(numberOfSteps):
	# 	stepIndex = "step" + str(stepNumber)
	# 	if stepIndex in steps.keys():
	# 		stepInfo = steps[stepIndex]
	# 		print("Step " + str(stepNumber) + ": ")
	# 		print("Ingredients: ")


	return

def toVegetarian():
	return

def fromVegetarian():
	return

def toHealthy():
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
