# Load dictionnary
wordlist = []
with open("dict.txt", "r") as f:
    for i in range(41147):
        wordlist.append(f.read(9)[:-1])

from random import randint

def choose_word(gletters, wletters, bletters, wordlist):
    sub_dict = []
    dict = wordlist[:]
    
    # Recherche des mots contenants au moins une bonne lettre
    for letter in "".join(list(set(wletters+gletters))):
        for word in dict:
            if letter in word:
                sub_dict.append(word)

    # Recherche des mots contenants toutes les lettres connues
    dict = []
    for word in sub_dict:
        if sum([1 for l in "".join(wletters+gletters)if l in word]) == len("".join(wletters+gletters)):
            dict.append(word)
    dict = list(set(dict))

    # Tri des mots s'ils contiennent une lettre bannies
    sub_dict = []
    for word in dict:
        if sum([1 for l in word if l in bletters]) == 0:
            sub_dict.append(word)
    sub_dict = list(set(sub_dict))

    # Tri des mots qui n'ont pas leurs lettres aux positions connues
    dict = []
    for word in sub_dict:
        if sum([1 for i in range(len(gletters))if gletters[i]!="" and gletters[i]==word[i]]) == len("".join(gletters)):
            dict.append(word)
    dict = list(set(dict))

    # Tri des mots qui ont une lettre la où elle ne peut être
    sub_dict = []
    for word in dict:
        if sum([1 for l in range(8)if word[l] != wletters[l]]) == 8:
            sub_dict.append(word)

    dict = list(set(sub_dict))

    del sub_dict
    return dict, dict

gletters = ['A', '', 'L', '', 'A', 'N', 'T', 'E']
wletters = ['', '', '', '', '', '', '', '']
bletters = ""

print(choose_word(gletters, wletters, bletters, wordlist)[0])