import requests
from bs4 import BeautifulSoup as bs
import amparser
from CheckAlbion2D import NUM_DETAILS, NAME_INDEX, PRICE_INDEX, WEBCODE_INDEX

filePath = "recipe_book.txt"
url_base = "https://www.albiononline2d.com"
web_extention = "/en/item/id/"

def getRecipe(item_code):
    recipe = []
    url = url_base + web_extention + item_code
    srccode = requests.get(url).text
    soup = bs(srccode, "html.parser")
    ingredients = soup.find_all("span",{"class":"item"})
    for i in ingredients:
        item = str(i)
        item_webcode = amparser.extractText(item, "img src", "/items/", ".png")[0]
        item_name = amparser.extractText(item, "title", "=\"", "\"/>")[0]
        item_count = amparser.extractText(item, "item-count", ">", "<")[0]
        recipe.append([item_webcode, item_name, item_count])
    return recipe

def setUpRecipe():
    try:
        file = open(filePath,"r")
        fileText = file.readlines()
        file.close()
        for lineNum in range(len(fileText)):
            if '#' not in fileText[lineNum] and fileText[lineNum] is not "\n":
                item = fileText[lineNum].split()
                recipe = getRecipe(item[WEBCODE_INDEX])
                print(recipe)
                for ingredientNum in range(len(recipe)):
                    recipe[ingredientNum][1] = recipe[ingredientNum][1].replace(" ", "_")
                    recipe[ingredientNum] = " ".join(recipe[ingredientNum])
                fileText[lineNum] = fileText[lineNum].replace("\n","") + " " + " ".join(recipe) + "\n"
                print(fileText)
        file = open(filePath,"w")
        file.write("".join(fileText))
        file.close()
    except:
        pass
                
            

setUpRecipe()









