import parseurl
from fractions import Fraction
import keywords
import nltk

url = "https://www.allrecipes.com/recipe/9703/crispy-gingersnaps/?internalSource=rotd&referringId=362&referringContentType=Recipe%20Hub"

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
        print(i.split())
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
                print(tagged_k)
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
            if (i in method_list or i+"ing" in method_list) and i not in methods:
                methods.append(i)

    return methods

def parse_steps(recipe_list):
    index1 = ""
    index2 = ""
    for index in range(len(recipe_list)):
        if recipe_list[index] == "Directions":
            index1 = index
        if recipe_list[index] == "You might also like":
            index2 = index
            break
    recipe_list = recipe_list[index1:index2]
    for i in recipe_list:
        if len(i.split())>2:
            print(i+"\n")

print(tag_ingredients(recipe_list))
print(find_tools(recipe_list))
print(get_cooking_methods(recipe_list))
parse_steps(recipe_list)
