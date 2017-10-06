from selenium import webdriver
import time

filePath = "monitored_prices.txt"
url_base = "https://www.albiononline2d.com/en/item/id/"
keyId = "Caerleon Market"
prefix = "<b>"
postfix = "</b>"
prices = []
browser = webdriver.PhantomJS()

NUM_DETAILS = 2
# extention price

def searchHtml(url):
    innerHTML = ""
    timesTried = 0
    while keyId not in innerHTML and timesTried < 5:
        browser.get(url)
        print("attempt :",timesTried)
        time.sleep(3)
        innerHTML = browser.execute_script("return document.body.innerHTML")
        timesTried += 1
    while keyId in innerHTML:
        currPos = innerHTML.find(keyId) + len(keyId)
        innerHTML = innerHTML[currPos:]
        startPos = innerHTML.find(prefix) + len(prefix)
        endPos = innerHTML.find(postfix)
        price_wanted = innerHTML[startPos:endPos]
        # print("CurrPos:",currPos," startPos:",startPos," EndPos:",endPos)
        return price_wanted
        #innerHTML = innerHTML[endPos+len(postfix):]

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
    for i in range(len(prices)):
        url = url_base + prices[i][0]
        print("Searching for "+prices[i][0])
        price_gotten = searchHtml(url)
        prices[i][1] = price_gotten
        print("Finished Searching\nPrice obtained is ",price_gotten)


def _save():
    file = open(filePath,"r")
    fileText = file.readlines()
    file.close()
    for i in prices:
        try:
            for j in range(len(fileText)):
                if i[0] in fileText[j] and i[1] is not None:
                    fileText[j] = i[0]+" "+i[1]+"\n"
                    break;
        except:
            pass
    file = open(filePath,"w")
    file.write("".join(fileText))
    file.close()
        
def printPrices():
    width = 30
    for i in prices:
        spacing = width - len(i[0])
        print(i[0]," "*spacing,i[1])
    

def main():
    _load()
    print("Load complete")
    getPrices()
    _save()
    printPrices()

if __name__ == '__main__':
    main()

browser.quit
