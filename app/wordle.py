# Christine Chen, Naomi Kurian, Ethan Cheung, Owen Zeng
# WheelOfFortune
# SoftDev
# P01 – ArRESTed Development
# 2025-12-22

import requests
import json
import random

def get_key():
    try:
        with open("keys/key_MerriamWebsterDictionary.txt", "r") as k:
            return k.read().strip()
    except:
        return ""

def get_valid_words():
    # Since we can't get random words from M-W API, we use a static list for targets
    # This list can be expanded
    return [
        "APPLE", "BEACH", "BRAIN", "BREAD", "BRUSH", "CHAIR", "CHEST", "CHORD",
        "CLICK", "CLOCK", "CLOUD", "DANCE", "DIARY", "DRINK", "DRIVE", "EARTH",
        "FEAST", "FIELD", "FRUIT", "GLASS", "GRAIN", "GRAPE", "GREEN", "GHOST",
        "HEART", "HOUSE", "JUICE", "LIGHT", "LEMON", "MELON", "MONEY", "MUSIC",
        "NIGHT", "OCEAN", "PARTY", "PHONE", "PIANO", "PILOT", "PLANE", "PLATE",
        "RADIO", "RIVER", "ROBOT", "SHIRT", "SHOES", "SMILE", "SNAKE", "SPACE",
        "SPOON", "STARS", "STORM", "SUGAR", "TABLE", "TASTE", "TIGER", "TOAST",
        "TOUCH", "TRAIN", "TRUCK", "VOICE", "WATCH", "WATER", "WHALE", "WORLD",
        "WRITE", "YOUTH", "ADIEU", "STERN", "AUDIO", "VIDEO", "GAMES", "REACT",
        "FLASK", "HELLO", "PIZZA", "SUSHI"
    ]

def check_word_exists(word):
    try:
        key = get_key()
        if not key:
            print("No API key found")
            return False

        cant = ["abbreviation", "combining form", "geographical name", "trademark", "biographical name", "symbol", "slang", "proper noun", "abbrev", "latin phrase"]

        url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word.lower()}?key={key}'

        response = requests.get(url)
        data = response.json()

        if not data:
            return False

        # Check if it's a valid word entry
        for item in data:
            if isinstance(item, dict):
                # Ensure it matches the requested word stem
                if "meta" in item and (word.lower() in item["meta"]["stems"]):
                     if "fl" in item:
                         if item["fl"] in cant:
                             continue
                         return True
                # Also check if the id matches the word directly (sometimes stems are weird)
                if "meta" in item and item["meta"]["id"].split(":")[0].lower() == word.lower():
                     if "fl" in item:
                         if item["fl"] in cant:
                             continue
                         return True

        return False

    except Exception as e:
        print(f"Validation Error: {e}")
        return False

def get_target_word(word_list):
    if not word_list:
        return "HELLO"
    return random.choice(word_list).upper()

def check_guess(guess, target):

    guess = guess.upper()
    target = target.upper()

    result = ["absent"] * 5
    target_counts = {}

    for char in target:
        target_counts[char] = target_counts.get(char, 0) + 1

    # green
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = "correct"
            target_counts[guess[i]] -= 1

    # yellow
    for i in range(5):
        if result[i] == "absent": # Not already marked correct
            letter = guess[i]
            if letter in target_counts and target_counts[letter] > 0:
                result[i] = "present"
                target_counts[letter] -= 1

    return result
