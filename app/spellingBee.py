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
    with open("keys/key_MerriamWebster.txt", "r") as k:
        return k.read().strip()

def randNums():
    letters = []
    for i in range(7):
        letters += [chr(random.randint(65, 90))]
    return letters

def checkword(word):
    key = get_key()
    with urllib.request.urlopen(f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/cat?key={key}') as response:
        js = response.read()
    l = json.loads(js) #coverts to dict
    dict = l[0]
    print(l)

    return 1

checkword(1)
print(randNums())
