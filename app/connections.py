import random
import urllib.request
import json

# <---------- API KEY LOADING ---------->

def get_MW_key():
    with open("keys/key_MerriamWebsterThesaurus.txt", "r") as k:
        return k.read().strip()

# <---------- Merriam Webster Thesaurus ---------->

def get_synonyms(word):
    key = get_MW_key()
    with urllib.request.urlopen(f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}") as response:
        data = json.loads(response.read())
    try:
        return data[0]["meta"]["syns"][0][:4]
    except:
        return []
    
def get_antonyms(word):
    key = get_MW_key()
    with urllib.request.urlopen(f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}") as response:
        data = json.loads(response.read())
    try:
        return data[0]["meta"]["ants"][0][:4]
    except:
        return []
