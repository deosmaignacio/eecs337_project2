import tagdata, keywords
import random

def vegetarian():
    # iterate through all meat keys, replace them with vegetarian keys
    dict = tagdata.tag_ingredients(recipe_list)
    for key in dict.keys():
        for meat in keywords.meat():
            if key == meat:
                dict[key] = dict.pop(random.choice(keywords.vegetarian()))
    return dict

print("Vegetarian Ingredients"+"\n",vegetarian(),"\n")
