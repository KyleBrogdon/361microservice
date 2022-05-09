from bs4 import BeautifulSoup
import requests
import time

# code citation for web scapers: https://arguswaikhom.medium.com/web-scraping-word-meaning-with-beautifulsoup-99308ead148a
# code citation for web scraper: https://www.byteacademy.co/blog/build-keyword-dictionary-python

# Loops continously while checking watchMe.txt to see if a word is input. If a
# word is input, it then calls createDefinitionFile and goes back to sleep
# waiting for the next word
def getDefinition():
    while True:
        while True:
            time.sleep(1.0)
            file = open("watchMe.txt", "r")
            data = file.readline().strip()
            file.close()
            if data is None or data == '':
                continue
            else:
                break
        wordToDefine = data
        scrape = "https://www.oxfordlearnersdictionaries.com/definition/english/" + wordToDefine
        headers = {"User-Agent": ""}
        response = requests.get(scrape, headers=headers)
        definedWord = None
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            result = soup.find_all('li', class_='sense')
            for x in result:
                definedWord = x.find('span', class_='def').text
                break  # stop at the first returned definition
        if definedWord is None or definedWord == '':  # error checking
            continue
        else:
            createDefinitionFile(wordToDefine, definedWord)


# Takes as strings the word that was defined in getDefinition, the returned value from
# getDefinition, and an optional argument of a path name, then creates a
# file in the specified directory in the format word.txt, containing the contents
# in definition. If path is left as none, this file is made in the same directory
# as definitions.py. Example of proper format of path (note trailing /) for a
# user creating the new file inside their OSU directory in documents = "users/documents/OSU/"
def createDefinitionFile(word, definition, path = None):
    if path is not None:
        filename = path + word + ".txt"
    else:
        filename = word + ".txt"
    with open(filename, "w") as f:
        f.write(definition)
    return

getDefinition()