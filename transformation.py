import tagdata, keywords
import random, parseurl, nltk

url = "https://www.allrecipes.com/recipe/223042/chicken-parmesan/?internalSource=previously%20viewed&referringContentType=Homepage&clickId=cardslot%206&fbclid=IwAR3uxS2ybMBJGijFYGSdqZoRkaS9lSYF82S5l35CPZSg9-M0R7FdDgHdTjA"
recipe_list = parseurl.processhtml(url)

def vegetarian():
    # iterate through all meat keys, replace them with vegetarian keys
    dict = tagdata.tag_ingredients(recipe_list)
    for key in dict.keys():
        print ("AGAIN HERE")
        print (key)
        # for meat in keywords.meat():
        if key == "cheese ":
            print ("HERE")
            # print (dict.pop(key))
            dict["onions for sale"] = dict[key]
            print (dict["onions for sale"])
            del dict[key]
            # random.choice(keywords.vegetarian())
    return dict

print("Vegetarian Ingredients"+"\n",vegetarian(),"\n")
