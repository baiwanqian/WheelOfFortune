#Christine Chen, Naomi Kurian, Ethan Cheung, Owen Zeng
#WheelOfFortune
#SoftDev
#P01 – ArRESTed Development
#2025-12-02

import random
import urllib.request
import json

#make accepted words, check words

def get_key():
    with open("keys/key_MerriamWebsterDictionary.txt", "r") as k:
        return k.read().strip()

def randNums():
    letters = []
    for i in range(7):
        letters += [chr(random.randint(65, 90))] #ASCII values for A-Z
    vowels = ['A', 'E', 'I', 'O', 'U']
    for i in range(2):
        letters[random.randint(0, 6)] = vowels[random.randint(0, 4)]
    return letters

def checkword(word):
    key = get_key()
    try:
        with urllib.request.urlopen(f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={key}') as response:
            js = response.read()
        l = json.loads(js) #coverts to dict
        d = l[0] #list of dictionaries -- now dictionary
        cant = ["abbreviation", "combining form", "geographical name", "trademark", "biographical name", "symbol", "slang"] #words that eist but don't meet requirements for game
        exists = True
        short = False
        if "meta" in d and "fl" in d: #"meta" is to check it's not a list of suggested words
            for typ in cant: 
                if d["fl"] == typ: #"fl" specifies what type of work
                    exists = False
            if len(word) <= 3:
                short = True #checks if word is too short
        else:
            exists = False
        #print(exists)
    except Exception as e:
        print("An error occurred")
        return [False, False, False] #second value says if ran without error
    return [exists, True, short]


#print(checkword("cat"))
#print(randNums())
