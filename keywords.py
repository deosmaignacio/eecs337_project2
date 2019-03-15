def measurements():
    words = ["cups","teaspoons","tablespoons","ounces","pounds","quarts","pints","gallons", "cans", "bottles"]
    return words

def tools():
    words = ["pans","ovens","skillets","knifes","spoons","forks","bowls","plates","cups","whisks"]
    words.extend(["graters","parchment papers","baking sheets", "sheets","peelers","tongs","measuring cups"])
    words.extend(["mashers","colanders","cutting boards","thermometers","mixers","zesters"])
    words.extend(["ricers","mandolines","slicers","bags","skewers","knives","cutters","corers"])
    words.extend(["pots","press","torchs","openers","trays","cheesecloths","chinois","pitters"])
    words.extend(["cleavers","clay pots","corkscrews","timers","scalers","funnels","ladles"])
    words.extend(["squeezers","reamers","grinders","tenderizers","mezzalunas","frothers","mortars","pestles"])
    words.extend(["gloves","blenders","mills","rolling pins","scales","scissors","scoops","sieves","spatulas"])
    words.extend(["tamis","boilers","processors","kettles","beanpots","pressure cookers","woks"])
    words.extend(["fryers","grillers","grills","steamers","makers","machines"])
    return words

def cooking_methods():
    words = ["al dente","amandine","au gratin","au jus","baghaar","bain-marie","bake","bard","barbecue","barbecuing","baste","basting","blanch","boil","braise","braising","brine","brining","broast","broil","browning","caramelize","casserole","charboil","chiffonade","stewing","velveting","coddling","conche","confit","creaming","croquette","curdling","cure","cured","curing","deep fry","deglaze","deglazing","degrease","degreasing","dredge","dry roast","dry","emulsify","en papillote","en vessie","engastration","ferment","flambe","fillet","foam","fondue","fricassee","frost","fry","fried","garnish","glaze","glazing","gratin","grill","hibachi","infuse","infusion","infusing","jugging","juicing","julienning","julienne","kalua","karaage","kho","kinpira","lard","maceration","marinate","marinating","macerate","mince","mincing","microwave","parbaking","parbake","parboil","pasteurize","pickle","pickling","poach","puree","proof","reduce","reduction","reducing","render","ricing","roast","rotisserie","roux","saute","score","scoring","sear","season","simmer","smoke","smoking","sour","smother","sous-vide","steam","steep","stir-fry","stew","stuff","tandoor","temper","tenderize","tenderizing","teriyaki","thermal","thicken","wok","zest","preheat","pre-heat","mix","sprinkle","coat","coating","drizzle"]
    return words

def time():
    words = ["minutes","seconds","hours","days"]
    return words

def meat():
    words = ["sausage", "chorizo sausage", "chuck roast", "roast", "chicken", "beef", "turkey", "ham", "steak", "fish", "pork", "bacon", "duck", "cod", "salmon", "sea bass", "tilapia", "clam", "clams", "mussel", "mussels", "scallop", "scallops", "lobster", "shrimp", "tuna", "abalone"]
    return words

def veggies():
    words = ["corn", "mushrooms", "squash", "lettuce", "carrots", "cucumbers", "celery", "spinach", "cabbage", "asparagus", "radish", "kale", "zucchini", "peas"]
    return words

def sandwich():
    words = ["bread", "rolls", "buns", "pita", "tortillas"]
    return words

def pasta():
    words = ["pasta", "spaghetti", "lasagna", "cannelloni", "macaroni", "ravioli", "rigatoni", "tagliatelle", "tortellini", "penne", "linguine", "fettucini", "pappardelle", "orzo", "bucatini", "vermicelli", "fusilli", "ziti", "rotini"]
    return words

def dressing():
    words = ["mayonnaise", "ketchup", "mustard", "dressing", "ranch", "cajun"]
    return words

# Vegetarian Options
def vegetarian():
    words = ["tofu", "tempeh", "seitan", "mushrooms","lentils"]
    return words

# Asian Foods
def asian_noodles():
    words = ["rice noodles", "udon", "soba", "ramen", "lo mein", "wonton noodles", "somen"]
    return words

def asian_sandwich():
    words = ["naan", "rice bread", "flatbread", "milk bread", "ddongbang"]
    return words

def asian_meat():
    words = ["wagyu beef", "bulgogi", "beef satay", "chicken satay", "pepper steak", "mongolian beef", "general tsao's chicken", "pork belly", "sesame chicken", "braised duck", "curry chicken"]
    return words

def asian_veggies():
    words = ["napa cabbage", "bok choy", "daikon", "white radish", "chinese eggplant", "choy sum", "mizuna", "lotus root", "taro", "chinese broccoli"]
    return words

def asian_dressing():
    words = ["sesame oil", "hoisin sauce", "soy sauce", "fish sauce", "plum sauce", "chili oil", "XO sauce"]
    return words

def asian_sugar():
    words = ["wasanbon sugar", "okinawa black sugar", "china rock honey sugar", "kurosato sugar"]
    return words

def asian_cheese():
    words = ["paneer", "sakura cheese", "bandel cheese", "ragya yak cheese"]
    return words
