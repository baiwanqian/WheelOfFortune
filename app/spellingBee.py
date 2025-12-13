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
    vowels = ['A', 'E', 'I', 'O', 'U', 'S']
    for i in range(3):
        letters[random.randint(0, 6)] = vowels[random.randint(0, 5)]
    return letters

def checkword(word, letter): #returns exists, ran smoothly, short, has letter
    print(letter)
    try:
        key = get_key() 
        short = False
        exists = False
        cant = ["abbreviation", "combining form", "geographical name", "trademark", "biographical name", "symbol", "slang", "proper noun", "abbrev", "latin phrase"] #words that eist but don't meet requirements for game
        hasLetter = letter in word
        with urllib.request.urlopen(f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={key}') as response:
            js = response.read()
        l = json.loads(js) #coverts to dict
        if not l:
            return [False, True, False, False] #when API returns empty list
        #print(l[1])

        for i in range(len(l)): #for each definition
            d = l[i] #list of dictionaries  meta not in every dict 
            print(d)
            if "meta" in d and (word.lower() in d["meta"]["stems"]): #"meta" is to check it's not a list of suggested words
                if "fl" in d:
                    print(d["fl"].lower() in cant)
                    if d["fl"] in cant: #"fl" specifies what type of work
                        continue
                    exists = True
                    break

        if len(word) <= 3:
            short = True #checks if word is too short
    except Exception as e:
        print("An error occurred")
        return [False, False, False, False] #second value says if ran without error
    return [exists, True, short, hasLetter] 


#print(checkword("cat"))
#print(randNums())
