'''
Helps parses the HTML file to yield the embedded price indicated after the
indicator and within the prefix and postfix.
'''
def _extractText(text, indicator, prefix, postfix):
    while indicator in text:
        indicatorIdx = text.find(indicator) + len(indicator)
        slicedText = text[indicatorIdx:]
        startIdx = slicedText.find(prefix) + len(prefix)
        endIdx = slicedText.find(postfix)
        text = text[indicatorIdx+endIdx+len(postfix):]
        yield slicedText[startIdx:endIdx]

def extractText(text, indicator, prefix, postfix):
    return list(_extractText(text, indicator, prefix, postfix))

def extractPrice(html, marketName):
    return list(extractText(html, marketName, "<b>", "</b>"))

def extractName(html):
    return list(extractText(html, 'class="notop"', "<span>", "</span>"))
