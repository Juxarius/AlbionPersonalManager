from selenium import webdriver
import time
import amparser

filePath = "monitored_prices.txt"
url_base = "https://www.albiononline2d.com/en/item/id/"
keyId = "Caerleon Market"
prefix = "<b>"
postfix = "</b>"
prices = []


NUM_DETAILS = 3

WEBCODE_INDEX = 0
NAME_INDEX = 1
PRICE_INDEX = 2
# extention name price

def getHtml(url):
    innerHTML = ""
    timesTried = 0
    while keyId not in innerHTML and timesTried < 3:
        browser.get(url)
        print("attempt :",timesTried)
        time.sleep(3)
        innerHTML = browser.execute_script("return document.body.innerHTML")
        timesTried += 1
    return innerHTML

def _load():
    file = open(filePath,"r")
    fileText = file.readlines()
    global prices
    for i in fileText:
        # to ignore if start with # or just an enter
        if '#' not in i and i[0] != '\n':
            details = i.split()
            while len(details) < NUM_DETAILS:
                details.append("")
            prices.append(details)
    file.close()

def getPrices():
    global prices
    global browser
    browser = webdriver.PhantomJS()
    for i in range(len(prices)):
        url = url_base + prices[i][0]
        print("Searching for "+prices[i][0])
        html = getHtml(url)
        prices[i][1] = amparser.extractName(html)[0].replace(" ","_")
        priceGotten = amparser.extractPrice(html, keyId)
        if len(priceGotten) > 0:
            prices[i][2] = priceGotten[0]
        print("Finished Searching\n", prices[i][1], "is", prices[i][2])


def _save():
    file = open(filePath,"r")
    fileText = file.readlines()
    file.close()
    for i in prices:
        try:
            for j in range(len(fileText)):
                if i[0] in fileText[j] and i[2] is not None:
                    fileText[j] = i[0]+" "+i[1]+" "+i[2]+"\n"
                    break;
        except:
            pass
    file = open(filePath,"w")
    file.write("".join(fileText))
    file.close()
        
def printPrices():
    width = 35
    for i in prices:
        spacing = width - len(i[NAME_INDEX])
        print(i[NAME_INDEX].replace("_"," ")," "*spacing,i[PRICE_INDEX])
    

def main():
    _load()
    print("Load complete")
    getPrices()
    _save()
    printPrices()

if __name__ == '__main__':
    main()

