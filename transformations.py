import tagdata, sys, parseurl, difflib, keywords, random, copy

originalDish = ""
originalIngredients = {}
originalSteps = {}
originalTools = []


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
	global recipeList
	global originalTools

	recipeList = parseurl.processhtml(url)
	originalDish = extractDishName(url)
	print(originalDish)

	ingredients = tagdata.tag_ingredients(recipeList)
	originalIngredients = ingredients
	print("Ingredients: ")
	tagdata.print_ingredients(recipeList)
	tools = tagdata.find_tools(recipeList)
	originalTools = tools
	methods = tagdata.get_cooking_methods(recipeList)
	print('\n')
	steps = tagdata.parse_steps(ingredients, tools, methods, recipeList)
	originalSteps = steps

	# print('\n')
	# print("Ingredients: ")
	# for ingredient in ingredients:
	# 	quantity = ingredients[ingredient]['quantity']
	# 	measurement = ingredients[ingredient]['measurement']
	# 	measurement = convertMeasurement(measurement)
	# 	descriptor = ingredients[ingredient]['descriptor']
	# 	if quantity == "":
	# 		print(str(measurement) + " " + ingredient + " " + str(descriptor))
	# 	else:
	# 		quantity = int(ingredients[ingredient]['quantity'])
	# 		print(str(quantity).strip() + " " + str(measurement).strip() + " " + ingredient + " " + str(descriptor).strip())

	print('\n')
	tagdata.print_tools(recipeList)
	print('\n')

	# print("Main cooking method: " + determineCookingMethod(methods))
	tagdata.print_methods(recipeList)
	tagdata.print_directions(recipeList)

def main():
	url = input("Enter allRecipes.com URL:" + '\n')
	print("--------------------------------")
	originalRecipe(url)
	print("--------------------------------")
	while True:
		transformation = int(input("Select one: " + '\n' + "1: To Vegetarian" + '\n' + "2: From Vegetarian" + '\n' + "3: To Healthy" + '\n' + "4: From Healthy" + '\n'+ "5: To Asian" + '\n'))
		if transformation == 1:
			toVegetarian()
		elif transformation == 2:
			fromVegetarian()
		elif transformation == 3:
			toHealthy()
		elif transformation == 4:
			fromHealthy()
		elif transformation == 5:
			toAsianCuisine()



	return

def toVegetarian():
	veg_dict = {}
	meat_list = keywords.meat()
	veg_list = keywords.vegetarian()
	relationship_dict = {}
	veg_random_list = []

	# If we find a meat, we change the key to a veggie and append new key to new dict
	for key in originalIngredients.keys():
		main_temp_str = ""
		veg_temp_str = ""
		for i in key.split():

			main_temp_str += i + " "

			if i in meat_list:
				index = random.randint(0,len(veg_list)-1)
				while index in veg_random_list:
					index = random.randint(0,len(veg_list)-1)
				veg_random_list.append(index)
				meat = i
				i = veg_list[index]
				relationship_dict.update({meat:i})
				veg_temp_str += i

		if veg_temp_str != "":
			veg_dict.update({veg_temp_str:originalIngredients[key]})
		else:
			veg_dict.update({main_temp_str:originalIngredients[key]})


	# Print ingredient dict
	for key, value in veg_dict.items():
		print("\t",value["quantity"],value["measurement"],value["descriptor"],key)

	# Change meats in the directions to correlate to veggies above
	dir = tagdata.get_directions(recipeList)
	dir = dir.split()
	meat_key = relationship_dict.keys()
	for word_index in range(len(dir)):
		word = dir[word_index]
		if word.strip(".,()") in meat_key:
			dir[word_index] = relationship_dict[word.strip(".,()")]

	# Print methods and tools
	tagdata.print_methods(recipeList)
	tagdata.print_tools(recipeList)

	# Print directions
	print("Directions:"+"\n")
	print(' '.join(str(m) for m in dir),"\n")
	return

def fromVegetarian():
	tagdata.print_ingredients(recipeList)
	tagdata.print_methods(recipeList)
	tagdata.print_tools(recipeList)
	tagdata.print_directions(recipeList)
	return

def toHealthy():
	global originalIngredients
	global originalTools
	global originalSteps
	healthyRecipe = copy.deepcopy(originalIngredients)

	unhealthyReplacements = {'burger': 'turkey burger', 'rice': 'brown rice', 'noodles': 'zoocchini noodles', 'pancetta': 'turkey ham', 'french fries': 'zucchini fries', 'fries': 'zucchini fries', 'pancake': 'banana pancakes', 'beef': 'turkey burger', 'fries': 'sweet potato fries', 'milk': 'skim milk', 'chocolate' : 'dark chocolate', 'yogurt': 'greek yogurt', 'ranch': 'olive oil', 'caesar': 'olive oil'}
	# replace cheeses with feta cheese (not all of them... doesn't make sense to replace parmesan in a pasta w/ feta cheese for instance)
	cheeseTypes = ['mozzarella', 'parmigiano-reggiano', 'parmigiano', 'parmigiano reggiano', 'goat', 'cheddar', 'american', 'monterey', 'jack', 'monterey jack', 'provolone', 'cheddar', 'brie', 'swiss', 'manchego', 'parmesan']
	# replace all breads with Whole wheat Bread
	breadTypes = ['bread', 'white', 'multigrain', 'cornbread', 'ciabatta', 'naan', 'brioche', 'brown', 'focaccia', 'bagel', 'pita', 'flatbread', 'breadsticks', 'roll']
	for originalIngredient in originalIngredients:
		ingredient = originalIngredient.replace(',', '')
		ingredientWords = ingredient.split()
		replacement = False
		for unhealthyFood in unhealthyReplacements.keys():
			if replacement:
				break
			for ingredientWord in ingredientWords:
				if replacement:
					break
				if len(ingredientWord) > 3:
					if ingredientWord in unhealthyFood:
						ingredientInfo = originalIngredients[originalIngredient]
						if ingredientInfo['descriptor'].strip() in "white": # this just handles white rice. only case where descriptor was problematic
							ingredientInfo['descriptor'] = ''
						del healthyRecipe[originalIngredient]
						healthyRecipe[unhealthyReplacements[unhealthyFood]] = ingredientInfo
						replacement = True
						break
					elif ingredientWord in cheeseTypes:
						ingredientInfo = originalIngredients[originalIngredient]
						del healthyRecipe[originalIngredient]
						healthyRecipe["feta cheese"] = ingredientInfo
						replacement = True
						break
					elif ingredientWord in breadTypes:
						ingredientInfo = originalIngredients[originalIngredient]
						del healthyRecipe[originalIngredient]
						healthyRecipe["wheat bread"] = ingredientInfo
						replacement = True
						break
					elif "sugar" in ingredientWord:
						ingredientInfo = originalIngredients[originalIngredient]
						currMeasurement = ingredientInfo['quantity']
						if currMeasurement:
							try:
								float(currMeasurement)
								ingredientInfo['quantity'] = str(float(currMeasurement)/2)
							except:
								pass
						healthyRecipe[ingredient] = ingredientInfo
						replacement = True
						break

	dir = tagdata.get_directions(recipeList)
	dir = dir.split()
	for word_index in range(len(dir)):
		word = dir[word_index]
		for unhealthyFood in unhealthyReplacements.keys():
			if word in unhealthyFood and len(word) > 3:
				dir[word_index] = unhealthyReplacements[unhealthyFood]

	print("--------------------------------")
	print("Healthy " + originalDish + '\n')
	print("Ingredients: " + '\n')
	for ingredient in healthyRecipe:
		quantity = healthyRecipe[ingredient]['quantity']
		measurement = healthyRecipe[ingredient]['measurement']
		measurement = convertMeasurement(measurement)
		descriptor = healthyRecipe[ingredient]['descriptor']
		if quantity == "":
			print(str(measurement) + " " + ingredient + " " + str(descriptor))
		else:
			quantity = float(healthyRecipe[ingredient]['quantity'])
			print(str(quantity).strip() + " " + str(measurement).strip() + " " + ingredient + " " + str(descriptor).strip())
	print('\n')
	tagdata.print_methods(recipeList)
	print('\n' + "Tools: " + '\n')
	for tool in originalTools:
		print(tool)
	print('\n')
	direction = ""
	for wordIndex in range(len(dir)):
		word = dir[wordIndex]
		if wordIndex < len(dir) - 1 and len(word) > 0 and word[0].isupper() and dir[wordIndex + 1][0].islower() and (dir[wordIndex -1][0].islower() or len(dir[wordIndex -1 ]) < 4):
			print(direction)
			direction = dir[wordIndex] + " "
		else:
			direction += dir[wordIndex] + " "
	if len(direction.strip()) > 0:
		print(direction)

	print("--------------------------------")
	return

def fromHealthy():
		global originalIngredients
		global originalTools
		global originalSteps
		healthyRecipe = copy.deepcopy(originalIngredients)

		unhealthyReplacements = {'turkey burger': 'beef burger', 'brow rice': 'white rice', 'zoocchini noodles': 'noodles', 'turkey ham': 'pancetta', 'fries': 'french fries', 'pancake': 'pancakes', 'sweet potato': 'french fries', 'skim milk': 'milk', 'dark chocolate' : 'milk chocolate', 'greek yogurt': 'yogurt', 'whole wheat': 'ciabatta', 'feta': 'cheddar'}
		for originalIngredient in originalIngredients:
			ingredient = originalIngredient.replace(',', '')
			ingredientWords = ingredient.split()
			replacement = False
			for unhealthyFood in unhealthyReplacements.keys():
				if replacement:
					break
				for ingredientWord in ingredientWords:
					if replacement:
						break
					if len(ingredientWord) > 3:
						if ingredientWord in unhealthyFood:
							ingredientInfo = originalIngredients[originalIngredient]
							if ingredientInfo['descriptor'].strip() in "brown": # this just handles brown rice. only case where descriptor was problematic
								ingredientInfo['descriptor'] = ''
							del healthyRecipe[originalIngredient]
							healthyRecipe[unhealthyReplacements[unhealthyFood]] = ingredientInfo
							replacement = True
							break
						elif "sugar" in ingredientWord:
							ingredientInfo = originalIngredients[originalIngredient]
							currMeasurement = ingredientInfo['quantity']
							if currMeasurement:
								try:
									float(currMeasurement)
									ingredientInfo['quantity'] = str(float(currMeasurement)*2)
								except:
									pass
							healthyRecipe[ingredient] = ingredientInfo
							replacement = True
							break

		dir = tagdata.get_directions(recipeList)
		dir = dir.split()
		for word_index in range(len(dir)):
			word = dir[word_index]
			for unhealthyFood in unhealthyReplacements.keys():
				if word in unhealthyFood and len(word) > 3 and word not in "heat":
					dir[word_index] = unhealthyReplacements[unhealthyFood]

		print("--------------------------------")
		print("Less Healthy " + originalDish + '\n')
		print("Ingredients: " + '\n')
		for ingredient in healthyRecipe:
			quantity = healthyRecipe[ingredient]['quantity']
			measurement = healthyRecipe[ingredient]['measurement']
			measurement = convertMeasurement(measurement)
			descriptor = healthyRecipe[ingredient]['descriptor']
			if quantity == "":
				print(str(measurement) + " " + ingredient + " " + str(descriptor))
			else:
				quantity = float(healthyRecipe[ingredient]['quantity'])
				print(str(quantity).strip() + " " + str(measurement).strip() + " " + ingredient + " " + str(descriptor).strip())
		print('\n')
		print("Methods: " + '\n' + "Fried")
		print('\n' + "Tools: " + '\n')
		for tool in originalTools:
			print(tool)
		print('\n')
		direction = ""
		for wordIndex in range(len(dir)):
			word = dir[wordIndex]
			if wordIndex < len(dir) - 1 and len(word) > 0 and word[0].isupper() and dir[wordIndex + 1][0].islower() and (dir[wordIndex -1][0].islower() or len(dir[wordIndex -1 ]) < 4):
				print(direction)
				direction = dir[wordIndex] + " "
			else:
				direction += dir[wordIndex] + " "
		if len(direction.strip()) > 0:
			print(direction)

		print("--------------------------------")
		return

def toIndianCuisine(): # or other style
	return

def toAsianCuisine():
	pan_list = ["pans","skillets","saucepans"]
	pot_list = ["pots"]
	oven_list = ["ovens"]
	asian_dict = {}

	# List of known food types
	veg_list = keywords.veggies()
	sandwich_list = keywords.sandwich()
	pasta_list = keywords.pasta()
	cheese_list = keywords.cheese()
	spices_list = keywords.spices()

	# List of asian food types
	asian_veggies_list = keywords.asian_veggies()
	asian_sandwich_list = keywords.asian_sandwich()
	asian_noodle_list = keywords.asian_noodles()
	asian_sugar_list = keywords.asian_sugar()
	asian_cheese_list = keywords.asian_cheese()
	asian_spices_list = keywords.asian_spices()

	# List of storing random integers
	random_list = []

	# List to use to change directions
	relationship_dict = {}

	# Find tools
	tools = tagdata.find_tools(recipeList)

	for key in originalIngredients.keys():

		# Use to check if we changed a word
		main_temp_str = ""
		meat_temp_str = ""
		veg_temp_str = ""
		sand_temp_str = ""
		pasta_temp_str = ""
		sugar_temp_str = ""
		cheese_temp_str = ""
		rem_cheese_temp_str = ""
		spices_temp_str = ""

		for i in key.split():
			i = i.strip(".,()")

			# used to reset current word to keep checking
			reset = i

			# unchanged key to check
			main_temp_str += i + " "

			# # if word is in veggie list
			random_list = []
			if i in veg_list or i+"s" in veg_list:
				index = random.randint(0,len(asian_veggies_list)-1)
				while index in random_list:
					index = random.randint(0,len(asian_veggies_list)-1)
				random_list.append(index)
				meat = i
				i = asian_veggies_list[index]
				relationship_dict.update({meat:i})
			veg_temp_str += i + " "

			i = reset
			random_list = []
			if i in sandwich_list or i+"s" in sandwich_list:
				index = random.randint(0,len(asian_sandwich_list)-1)
				while index in random_list:
					index = random.randint(0,len(asian_sandwich_list)-1)
				random_list.append(index)
				meat = i
				i = asian_sandwich_list[index]
				relationship_dict.update({meat:i})
			sand_temp_str += i + " "

			i = reset
			random_list = []
			if i in pasta_list or i+"s" in pasta_list:
				index = random.randint(0,len(asian_noodle_list)-1)
				while index in random_list:
					index = random.randint(0,len(asian_noodle_list)-1)
				random_list.append(index)
				meat = i
				i = asian_noodle_list[index]
				relationship_dict.update({meat:i})
			pasta_temp_str += i + " "

			i = reset
			random_list = []
			if i == "sugar":
				index = random.randint(0,len(asian_sugar_list)-1)
				while index in random_list:
					index = random.randint(0,len(asian_sugar_list)-1)
				random_list.append(index)
				meat = i
				i = asian_sugar_list[index]
				relationship_dict.update({meat:i})
			sugar_temp_str += i + " "

			i = reset
			random_list = []
			if i == "cheese":
				str_list = cheese_temp_str.split()
				for check_cheese in str_list:
					if check_cheese in cheese_list:
						str_list.remove(check_cheese)
						cheese_temp_str = ' '.join(str(m) for m in str_list)
				index = random.randint(0,len(asian_cheese_list)-1)
				while index in random_list:
					index = random.randint(0,len(asian_cheese_list)-1)
				random_list.append(index)
				meat = i
				i = asian_cheese_list[index]
				relationship_dict.update({meat:i})
			cheese_temp_str += i + " "

			i = reset
			random_list = []
			if i in spices_list:
				index = random.randint(0,len(asian_spices_list)-1)
				while index in random_list:
					index = random.randint(0,len(asian_spices_list)-1)
				random_list.append(index)
				meat = i
				i = asian_spices_list[index]
				relationship_dict.update({meat:i})
			spices_temp_str += i + " "


		# only update dict with changed str if something changed
		if main_temp_str != veg_temp_str:
			asian_dict.update({veg_temp_str:originalIngredients[key]})
		elif main_temp_str != sand_temp_str:
			asian_dict.update({sand_temp_str:originalIngredients[key]})
		elif main_temp_str != pasta_temp_str:
			asian_dict.update({pasta_temp_str:originalIngredients[key]})
		elif main_temp_str != sugar_temp_str:
			asian_dict.update({sugar_temp_str:originalIngredients[key]})
		elif main_temp_str != cheese_temp_str:
			asian_dict.update({cheese_temp_str:originalIngredients[key]})
		elif main_temp_str != spices_temp_str:
			asian_dict.update({spices_temp_str:originalIngredients[key]})
		else:
			asian_dict.update({main_temp_str:originalIngredients[key]})

	# change tools to asian tools
	for index in range(len(tools)):
		if tools[index] in pan_list or tools[index]+"s" in pan_list:
			meat = tools[index]
			tools[index] = "wok"

		if tools[index] in pot_list or tools[index]+"s" in pot_list:
			meat = tools[index]
			tools[index] = "clay pot"

		if tools[index] in oven_list or tools[index]+"s" in oven_list:
			meat = tools[index]
			tools[index] = "furnace"


	# print ingredients
	for key, value in asian_dict.items():
		print("\t",value["quantity"],value["measurement"],value["descriptor"],key)

	# change words in directions
	dir = tagdata.get_directions(recipeList)
	dir = dir.split()
	meat_key = relationship_dict.keys()
	for word_index in range(len(dir)):
		word = dir[word_index]
		word = word.lower()
		if word in pan_list or word+"s" in pan_list:
			meat = word
			dir[word_index] = "wok"

		if word in pot_list or word+"s" in pot_list:
			meat = word
			dir[word_index] = "clay pot"

		if word in oven_list or word+"s" in oven_list:
			meat = word
			dir[word_index] = "furnace"

		if word in cheese_list:
			dir[word_index] = ""

		if word.strip(".,()") in meat_key:
			dir[word_index] = relationship_dict[word.strip(".,()")]

	tagdata.print_methods(recipeList)
	print("Tools:"+"\n")
	for tool in tools:
		print("\t",tool)

	print("Directions:"+"\n")
	print(' '.join(str(m) for m in dir),"\n")
	return

def DIY():
	return

def cookingMethod(): # i.e. from bake to stir fry
	return

if __name__ == '__main__':
	main()
