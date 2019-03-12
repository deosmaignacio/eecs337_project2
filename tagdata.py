import parseurl
from fractions import Fraction
import keywords
import nltk

url = "https://www.allrecipes.com/recipe/223042/chicken-parmesan/?internalSource=previously%20viewed&referringContentType=Homepage&clickId=cardslot%206&fbclid=IwAR3uxS2ybMBJGijFYGSdqZoRkaS9lSYF82S5l35CPZSg9-M0R7FdDgHdTjA"
recipe_list = parseurl.processhtml(url)

def tag_ingredients(recipe_list):
	ingredients_dict = {}
	index1 = ""
	index2 = ""
	for index in range(len(recipe_list)):
		if recipe_list[index] == "Note: Recipe directions are for original size.":
			index1 = index
		if recipe_list[index] == "Add all ingredients to list":
			index2 = index
			break
	ingredients_list = recipe_list[index1+1:index2]

	measure_key_list = keywords.measurements()

	for i in ingredients_list:
		quantity = 0
		measurement = ""
		ingredient = ""
		descriptor = ""
		for k in i.split():
			if "/" in k:
				quantity += float(sum(Fraction(s) for s in k.split()))
			if k.isdigit():
				quantity += float(k)
			if k in measure_key_list or k+"s" in measure_key_list:
				measurement = k
			if k != quantity and k!= measurement and not(k.isdigit()) and not("/" in k):
				token_k= k.split()
				tagged_k = nltk.pos_tag(token_k)
				# print(tagged_k)
				if tagged_k[0][1] == "NN" or tagged_k[0][0] == "olive":
					ingredient += k + " "
				if (tagged_k[0][1] == "JJ" or tagged_k[0][1] == "VBN" or tagged_k[0][1] == "RB") and tagged_k[0][0] not in ingredient:
					descriptor += k + " "

		ingredients_dict.update({ingredient:{"quantity":quantity, "measurement":measurement,"descriptor":descriptor}})

	return ingredients_dict

def find_tools(recipe_list):
	tool_list = keywords.tools()
	index1 = ""
	tools = []
	for index in range(len(recipe_list)):
		if recipe_list[index] == "Directions":
			index1 = index
	recipe_list = recipe_list[index1:]

	for j in recipe_list:
		for i in j.split():
			i = i.strip(",.")
			i = i.lower()
			if (i in tool_list or i+"s" in tool_list) and i not in tools:
				tools.append(i)

	return tools

def get_cooking_methods(recipe_list):
	method_list = keywords.cooking_methods()
	index1 = ""
	methods = []
	for index in range(len(recipe_list)):
		if recipe_list[index] == "Directions":
			index1 = index
	recipe_list = recipe_list[index1:]

	for j in recipe_list:
		for i in j.split():
			i = i.strip(",.")
			i = i.lower()
			if (i in method_list or i+"ing" in method_list) and i not in methods:
				methods.append(i)

	return methods

def parse_steps(ingredient_dict, tool_list, method_list, recipe_list):
	time_list = keywords.time()
	ingredient_list= list(ingredient_dict.keys())
	index1 = ""
	index2 = ""
	steps_dict = {}
	for index in range(len(recipe_list)):
		if recipe_list[index] == "Directions":
			index1 = index
		if recipe_list[index] == "You might also like":
			index2 = index
			break
	recipe_list = recipe_list[index1:index2]
	count = 1
	for i in recipe_list:
		i = i.lower()
		i = i.split()
		if len(i)>2:
			steps_dict.update({"step{0}".format(count):{"ingredients":[],"tools":[],"methods":[],"times":[]}})
			for index in range(len(i)):
				i[index] = i[index].strip(",.")
				for k in ingredient_list:
					if (i[index] in k.split() or i[index]+"s" in k.split() or i[index][:-1] in k.split()) and i[index] not in steps_dict["step{0}".format(count)]["ingredients"]:
						steps_dict["step{0}".format(count)]["ingredients"].append(i[index])
				if (i[index] in tool_list or i[index]+"s" in tool_list or i[index][:-1] in tool_list) and i[index] not in steps_dict["step{0}".format(count)]["tools"]:
					steps_dict["step{0}".format(count)]["tools"].append(i[index])
				elif (i[index] in method_list or i[index]+"s" in method_list or i[index][:-1] in method_list) and i[index] not in steps_dict["step{0}".format(count)]["methods"]:
					steps_dict["step{0}".format(count)]["methods"].append(i[index])
				elif i[index] == "degrees":
					temp_str = ""
					if i[index-1].strip("()").isdigit():
						temp_str += i[index-1]

					temp_str += " degrees "

					if len(i[index+1].strip("().")) == 1:
						temp_str += i[index+1]

					steps_dict["step{0}".format(count)]["methods"].append(temp_str.strip("()."))

				elif (i[index] in time_list or i[index]+"s" in time_list or i[index][:-1] in time_list) and i[index] not in steps_dict["step{0}".format(count)]["times"]:
					temp_count = 1
					temp_str = i[index]
					while True:
						if i[index-temp_count].isdigit() or i[index-temp_count] == "to":
							temp_str = i[index-temp_count] + " " + temp_str
						else:
							break
						temp_count += 1

					steps_dict["step{0}".format(count)]["times"].append(temp_str)
			count += 1
	return steps_dict

print("Ingredients"+"\n",tag_ingredients(recipe_list),"\n")
print("Tools"+"\n",find_tools(recipe_list),"\n")
print("Methods"+"\n",get_cooking_methods(recipe_list),"\n")
ingredients = tag_ingredients(recipe_list)
tools = find_tools(recipe_list)
methods = get_cooking_methods(recipe_list)
print("Steps"+"\n",parse_steps(ingredients, tools, methods, recipe_list))
