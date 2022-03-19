import cv2
import numpy as np
import pyautogui as pg
from time import sleep
from random import randint
import keyboard

case_size = 52

# Chargement du dictionnaire
wordlist = []
with open("dict.txt", "r") as f:
    for i in range(41147):
        wordlist.append(f.read(9)[:-1])

def calibrate():
    # Detection du repère
    origin = pg.locateOnScreen("calibrage.png", confidence=0.9)
    return origin 

def check(origin, step): 
    case = (origin.left-110, origin.top-400+case_size*step)
    o = []
    for i in range(8):
        if list(screen[case[1], case[0]])[0] >= 180: o.append(0)
        elif list(screen[case[1], case[0]])[2] >= 180: o.append(1)
        else: o.append(2)
        case = (case[0]+case_size, case[1])
    return o

def choose_word(gletters, wletters, bletters, words):
    sub_dict = []
    dict = words[:]
    
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
    try:
        answer = dict.pop(randint(0, len(dict)-1))
    except:
        return "NO"
    return answer, dict

def submit_word(word):
    text_calib = pg.locateOnScreen("repere.png", confidence=0.9)

    pg.moveTo(text_calib.left+172, text_calib.top+128)
    pg.leftClick()
    pg.write(word, 0.01)
    pg.press("enter")

sleep(1)
nb_words = 0
nb_loose = 0
nb_win = 0

# Boucle principal
while True:

    # (RE)LANCEMENT DE LA PARTIE
    pg.moveTo(pg.locateOnScreen("calibrage.png", confidence=0.9))
    pg.leftClick()

    nb_words += 1
    print("###################################")
    print("PARTIES JOUÉES : " + str(nb_words))
    print("PARTIES GAGNÉES : " + str(nb_win))
    print("PARTIES PERDUES : " + str(nb_loose))

    sleep(1)

    step = 0
    word = ""
    bletters = ""

    for i in range(97, 119):
        screen = pg.screenshot()
        if pg.locateOnScreen(f"lettres/{chr(i)}.png", confidence=0.98) != None:
            first_letter = chr(i).upper()
            break
    
    # Recherche d'une solution
    answer, dict = choose_word([first_letter], [''for _ in 8*'_'], [], wordlist)
    # Écriture de la solution
    submit_word(answer)

    word = answer[:]

    #################################################################################
    #################################################################################
    #################################################################################

    # Boucle de résolution
    while True:
        sleep(0.2)

        # Calibrage
        screen = pg.screenshot()
        screen = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2RGB)
        origin = calibrate()

        # Analyse des couleurs
        errors = check(origin, step)

        # Vérification de l'état du jeu
        if check(origin, 7) == [2 for _ in range(8)]:
            nb_win += 1
            break
        elif check(origin, 7) == [0 for _ in range(8)]:
            nb_loose += 1
            break

        # Analyse des résultats
        gletters = ['' for _ in 8*'_']
        wletters = ['' for _ in 8*'_']

        for i in range(8):
            if errors[i] == 2: gletters[i] = word[i]
            elif errors[i] == 1: wletters[i] = word[i]
            elif not word[i] in wletters and not word[i] in gletters: bletters += word[i]

        # Tri de la liste des lettres bannies
        bletters = "".join(list(set(bletters)))
        for l in "".join(list(set(gletters+wletters))):
            bletters = bletters.replace(l, "")

        # Recherche d'une solution
        answer, dict = choose_word(gletters, wletters, bletters, dict)
        if answer == "NO":
            nb_loose += 1
            break
        # Écriture de la solution
        submit_word(answer)

        sleep(0.5)

        # Prise d'un screen
        screen = pg.screenshot()

        screen = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2RGB)
        origin = calibrate()
        # Vérification de la validité du mot
        if check(origin, step+1)[0] == 2:
            word = answer[:]
            step += 1
        
        # Vérification de la fin du Jeu
        if keyboard.is_pressed('escape'):
            exit()
