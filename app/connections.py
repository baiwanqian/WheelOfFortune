import random
import urllib.request
import json

# <---------- API Calls ---------->

def get_rand_topic():
    try:
        with urllib.request.urlopen("https://random-words-api.kushcreates.com/api?words=1") as response:
            data = json.loads(response.read())
        return data[0]
    except:
        print("An error occurred")
        return None

def get_related_words():
    try:
        with urllib.request.urlopen("https://api.datamuse.com/words?ml={topic}&max=4") as response:
            data = json.loads(response.read())
        words = []
        for i in data:
            words.append(i["word"])
        return words
    except:
        print("An error occurred")
        return []

# <----------  ---------->

def build_group():

def build_board():
