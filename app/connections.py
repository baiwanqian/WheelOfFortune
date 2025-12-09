import random
import urllib.request
import json

# <-------— API KEY LOADING -------—>

def get_MW_key():
    with open("keys/key_MerriamWebster.txt", "r") as k:
        return k.read().strip()

# 

def get_synonyms(word):
    key = get_MW_key()
    with urllib.request.urlopen(f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}") as response:
        data = json.loads(response.read())
    try:
        return data[0]["meta"]["syns"][0][:4]
    except:
        return []
