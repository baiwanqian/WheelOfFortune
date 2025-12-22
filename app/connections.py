# Christine Chen, Naomi Kurian, Ethan Cheung, Owen Zeng
# WheelOfFortune
# SoftDev
# P01 – ArRESTed Development
# 2025-12-22

import random
import urllib.request
import json

# <---------- API Calls ---------->

def get_rand_topic():
    try:
        with urllib.request.urlopen("https://random-words-api.kushcreates.com/api?words=1") as response:
            data = json.loads(response.read())
        word = data[0].get("word", "").lower()

        if data[0].get("language", "") != "en":
            return None
        if data[0].get("category", "") in {"wordle", "games", "brainrot"}:
            return None
        if not word.isalpha():
            return None

        return word
    except:
        print("An error occurred")
        return None

def get_related_words(topic):
    try:
        with urllib.request.urlopen(f"https://api.datamuse.com/words?ml={topic}&max=10") as response:
            data = json.loads(response.read())
        words = []
        for i in data:
            w = i["word"].lower()
            if w.isalpha():
                words.append(w)
        return words
    except:
        print("An error occurred")
        return []

# <---------- Connections Logic ---------->
fallback_topics = [
    "weather", "food", "color", "animal", "travel", "nature", "place", "movie"
]

def build_group():
    for i in range(10):
        topic = get_rand_topic()
        if not topic:
            topic = random.choice(fallback_topics)
        words = get_related_words(topic)
        if len(words) >= 4:
            chosen = []
            while len(chosen) < 4: # pick 4 unique random words if there are more than 4
                idx = random.randint(0, len(words) - 1)
                word = words[idx]
                if word not in chosen:
                    chosen.append(word)
            return topic, chosen
    print("An error occured")
    return None, []

def build_board():
    groups = []
    used = []
    attempts = 0
    while len(groups) < 4 and attempts < 50:
        attempts += 1
        topic, words = build_group()
        if topic:
            duplicate = False
            for w in words:
                if w in used:
                    duplicate = True
            if not duplicate:
                groups.append([topic, words])
                for w in words:
                    used.append(w)
    if len(groups) < 4:
        print("ERROR: Could not generate full Connections board.")
        return {
            "board": ["ERROR"] * 16,
            "groups": []
        }

    board = []
    for g in groups:
        for w in g[1]:
            board.append(w)

    random.shuffle(board)

    return {
        "board": board,
        "groups": groups
    }
