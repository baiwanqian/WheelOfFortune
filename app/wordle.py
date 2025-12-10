import urllib.request
import json
import random

def get_valid_words():
    try:
        url =    "https://random-words-api.kushcreates.com/api?language=en&category=wordle&length=5"

        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read()
            json_data = json.loads(data)
            
            words = []
            if isinstance(json_data, list):
                for item in json_data:
                    if isinstance(item, dict) and 'word' in item:
                        words.append(item['word'].upper())
                    elif isinstance(item, str):
                        words.append(item.upper())
            
            if words:
                return words
                
    except Exception as e:
        print(f"Wordle API Error: {e}")
    
    defaults = ["HELLO", "WORLD", "REACT", "FLASK", "AUDIO", "VIDEO", "GAMES", "PIANO", "STERN", "ADIEU"]
    return defaults

def get_target_word(word_list):

    if not word_list:
        return "HELLO" # Fallback
    return random.choice(word_list).upper()

def check_guess(guess, target):

    guess = guess.upper()
    target = target.upper()
    
    result = ["absent"] * 5
    target_counts = {}
    
    # Count frequency of letters in target
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