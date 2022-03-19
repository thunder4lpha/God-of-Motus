import requests as req
import codecs
from bs4 import BeautifulSoup
import unidecode

wordlist = []
with open("dict.txt", "r") as f:
    for i in range(41147):
        wordlist.append(f.read(9)[:-1])

'''
with codecs.open("dict.txt", "w+", "utf-8") as f:
    for x in range(97, 123):
        url = f'https://www.liste-de-mots.com/mots-nombre-lettre/8/{chr(x)}/'

        response = req.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        words = str(soup.findAll('p', class_="liste-mots")).split(", ")[1:-1]
        new_words = []
        for i in words:
            if not '-' in i:
                new_words.append(unidecode.unidecode(i).upper())
        f.write(" ".join(new_words))
        f.write(" ")
'''