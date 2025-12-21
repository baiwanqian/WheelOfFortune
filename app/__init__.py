# Christine Chen, Naomi Kurian, Ethan Cheung, Owen Zeng
# WheelOfFortune
# SoftDev
# P01 – ArRESTed Development
# 2025-12-02

import sqlite3
import random
from flask import Flask, render_template
from flask import session, request, redirect
import os
import requests

# <---- Mini Games ---->
import spellingBee
import wordle
import connections
import ingredients


# Flask
app = Flask(__name__)
app.secret_key = "bdzfgetdzhezt"

# SQLite
DB_FILE = "data.db"


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# database creation
db = get_db()
c = db.cursor()

c.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    xp INTEGER,
    level INTEGER)
    """
)

c.execute(
    """
    CREATE TABLE IF NOT EXISTS creatures (
    creature_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    rarity TEXT,
    xp INTEGER,
    level INTEGER,
    species TEXT,
    status TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id))
    """
)

db.commit()
db.close()

# Global variables for spelling bee
word = ""
score = 0
goodWords = []
lttrs = spellingBee.randNums()
submitted = 0

# Globals for rewards
species = "chicken"
lev = 1
animals = 0


# HTML PAGES
# LANDING PAGE
@app.route("/", methods=["GET", "POST"])
def homepage():
    if not "user_id" in session:
        return redirect("/login")
    else:
        return render_template("home.html", background_img=str(bg_file()))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usernames = [row[0] for row in fetch("users", "TRUE", "username")]
        if not request.form["username"] in usernames:
            return render_template(
                "login.html",
                error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>",
            )
        elif (
            request.form["password"]
            != fetch("users", "username = ?", "password", (request.form["username"],))[
                0
            ][0]
        ):
            return render_template(
                "login.html",
                error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>",
            )
        else:
            session["user_id"] = fetch(
                "users", "username = ?", "user_id", (request.form["username"],)
            )[0][0]
    if "user_id" in session:
        return redirect("/")
    session.clear()
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect("/")
    if request.method == "POST":
        usernames = [row[0] for row in fetch("users", "TRUE", "username")]
        if request.form["username"] in usernames:
            return render_template(
                "register.html",
                error="Username already taken, please try again! <br><br>",
            )
        elif request.form["password"] != request.form["confirm"]:
            return render_template(
                "register.html", error="Passwords don't match! <br><br>"
            )
        else:
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            c.execute("SELECT COUNT(*) FROM users")
            u_id = c.fetchall()[0][0]
            c.execute(
                "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                (
                    u_id,
                    request.form["username"],
                    request.form["password"],
                    0,
                    0,
                ),
            )
            db.commit()
            session["user_id"] = fetch(
                "users", "username = ?", "user_id", (request.form["username"],)
            )[0][0]
            db.close()
            return redirect("/")
    return render_template("register.html")


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    # db = get_db()
    # c = db.cursor()

    user = fetch("users", "user_id = ?", "*", (session["user_id"],))[0]
    creatures = fetch("creatures", "user_id = ?", "*", (session["user_id"],))

    # c.execute("SELECT * FROM users WHERE user_id = ?", (session["user_id"],))
    # user = c.fetchone()
    # c.execute("SELECT * FROM creatures WHERE user_id = ?", (session["user_id"],))
    # creatures = c.fetchall()

    # db.close()

    return render_template(
        "profile.html",
        username=user[1],
        xp=user[3],
        level=user[4],
        creatures=creatures,
        # background_img = "/static/background_images/cloudy_weather/OIP-657791057.jpeg"
        background_img=str(bg_file()),
    )


@app.route("/rewards", methods=["GET", "POST"])
def rewards():
    #global species, lev, animals
    #print("AAAAAAAAAAAAAAAA")
    #print(request.method)
    #print(request.form)
    if not 'user_id' in session:
        return redirect("/login")
    species = None
    lev = None
    if request.method == "POST":
        if request.form.get("action") == "h":
            species = random.choice(["chicken", "greenBird"])
            lev = 1
            hatch(species, lev)
        return redirect("/rewards")

    creatures = fetch("creatures", "user_id = ?", "*", (session["user_id"],))
    level = fetch("users", "user_id = ?", "level", (session["user_id"],))[0][0]
    canHatch = (level % 5 == 0) and level > 0
    print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
    return render_template("rewards.html", creatures = creatures, background_img = str(bg_file()), species = species, level = lev, canHatch = canHatch)


headers = {'IDontKnowWhatTheNameIs' : 'WheelOfFortune'}

STUY_LAT = 40.7127
STUY_LON = -74.0061


def currentWeather():
    # gets data at lat and lon coordinates
    try:
        endpoint = f"https://api.weather.gov/points/{STUY_LAT},{STUY_LON}"
        print(STUY_LAT)
        print(STUY_LON)
        print(endpoint)
        response = requests.get(endpoint, headers=headers)
        data = response.json()

        # gets all links about at pt (hourly daily etc)
        links = data["properties"]["forecastGridData"]
        print(links)

        # gets link relating to daily forecast at pt
        forecast_link = data["properties"]["forecast"]
        print(forecast_link)

        # retrieves forecast data at coordinates
        forecast_response = requests.get(forecast_link, headers=headers)
        forecast_data = forecast_response.json()
        # print(forecast_data)

        # gets most recently updated forecast for next period (for example: Monday, Monday Night, Tuesday, etc.)
        forecast = forecast_data["properties"]["periods"][0]["shortForecast"]
        print(forecast)
        return forecast
    except:
        print("An error occured")
        return "Unknown"


def bg_file():
    basepath = "./static/background_images"
    randFold = random.choice(os.listdir(basepath))
    basepath = (
        basepath + "/" + os.path.basename(randFold)
    )  # gives basepath to random folder (will change if key word found in API)
    print("before basepath: " + basepath)
    print(os.listdir(basepath))

    current_weather = currentWeather().lower()

    print("current weather: " + currentWeather())

    if (
        "sunny" in current_weather
        or "sun" in current_weather
        or "clear" in current_weather
    ):
        basepath = "./static/background_images/sunny_weather"
    if "cloudy" in current_weather or "clouds" in current_weather:
        basepath = "./static/background_images/cloudy_weather"
    if "rainy" in current_weather or "rain" in current_weather:
        basepath = "./static/background_images/rainy_weather"
    if "snowy" in current_weather or "snow" in current_weather:
        basepath = "./static/background_images/snowy_weather"
    if "unknown" in current_weather:
        basepath = "./static/background_images/unknown_weather"

    print("basepath: " + basepath)

    image = random.choice(os.listdir(basepath))

    print("image: " + image)

    path = basepath + "/" + os.path.basename(image)

    print("path:" + path)

    return path


#
def add_xp(user_id, amount):
    cur = fetch("users", "user_id = ?", "xp", (user_id,))[0][0]
    newXP = cur + amount
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(
        "UPDATE users SET xp = ? WHERE user_id = ?",
        (
            newXP,
            user_id,
        ),
    )
    c.execute(
        "UPDATE users SET level = ? WHERE user_id = ?",
        (
            (newXP // 50),
            user_id,
        ),
    )
    db.commit()
    db.close()


# <-------------------- MINIGAMES -------------------->
@app.route("/wordle", methods=["GET", "POST"])
def wordlePage():
    if not "user_id" in session:
        return redirect("/login")

    if "wordle_target" not in session or (
        request.method == "POST" and "new_game" in request.form
    ):
        words = wordle.get_valid_words()
        session["wordle_target"] = wordle.get_target_word(words)
        session["wordle_guesses"] = []
        session["wordle_status"] = "playing"
        session["wordle_message"] = ""
        if request.method == "POST":
            return redirect("/wordle")

    if request.method == "POST":
        guess = request.form.get("guess", "").strip().upper()
        guesses = session.get("wordle_guesses", [])
        target = session.get("wordle_target")
        status = session.get("wordle_status")

        if status != "playing":
            pass  # Game over
        elif len(guess) != 5:
            session["wordle_message"] = "Word must be 5 letters."
        else:
            # Validate
            # words = wordle.get_valid_words()
            if not wordle.check_word_exists(guess):
                session["wordle_message"] = "Not in word list."
            elif any(g[0] == guess for g in guesses):
                session["wordle_message"] = "Already guessed."
            else:
                feedback = wordle.check_guess(guess, target)
                guesses.append((guess, feedback))
                session["wordle_guesses"] = guesses
                session["wordle_message"] = ""

                if guess == target:
                    session["wordle_status"] = "won"
                    session["wordle_message"] = "You Won! \n+10 xp!"
                    add_xp(session["user_id"], 30)
                elif len(guesses) >= 6:
                    session["wordle_status"] = "lost"
                    session["wordle_message"] = f"Game Over! Word was {target}"

    keyboard_status = {}
    current_guesses = session.get("wordle_guesses", [])

    for g_word, g_feedback in current_guesses:
        for i, letter in enumerate(g_word):
            current_status = keyboard_status.get(letter, "empty")
            new_status = g_feedback[i]

            if current_status == "correct":
                continue
            elif current_status == "present":
                if new_status == "correct":
                    keyboard_status[letter] = "correct"
            elif current_status == "absent":
                if new_status == "correct":
                    keyboard_status[letter] = "correct"
                elif new_status == "present":
                    keyboard_status[letter] = "present"
            else:  # empty
                keyboard_status[letter] = new_status

    return render_template(
        "wordle.html",
        guesses=session.get("wordle_guesses", []),
        status=session.get("wordle_status", "playing"),
        message=session.get("wordle_message", ""),
        keyboard_status=keyboard_status,
    )


@app.route("/connections", methods=["GET", "POST"])
def connectionsPage():
    if not "user_id" in session:
        return redirect("/login")
    if "connections_board" not in session:
        game = connections.build_board()
        session["connections_board"] = game["board"]
        session["connections_groups"] = game["groups"]
        session["connections_all_groups"] = game["groups"][:]
        session["connections_selected"] = []
        session["connections_error"] = game.get("error", "")

        session["connections_mistakes"] = 4
        session["connections_solved_groups"] = []
        session["connections_status"] = "playing" # playing/win/lose
        session["connections_xp"] = 0
    board = session["connections_board"]
    groups = session["connections_groups"]
    selected = session["connections_selected"]
    error = session.get("connections_error", "")
    msg = ""
    solved_groups = session["connections_solved_groups"]

    if request.method == "POST" and "play_again" in request.form:
        # play again
        reset = [
            "connections_board",
            "connections_groups",
            "connections_all_groups",
            "connections_selected",
            "connections_error",
            "connections_mistakes",
            "connections_solved_groups",
            "connections_status",
            "connections_xp"
        ]
        for r in reset:
            session.pop(r, None)
        return redirect("/connections")

    if request.method == "POST" and session["connections_status"] == "playing":
        # shuffle button
        if "shuffle" in request.form:
            random.shuffle(board)
            session["connections_board"] = board
        # deselect button
        elif "deselect" in request.form:
            selected = []
            session["connections_selected"] = selected
        # clicking word
        elif "choice" in request.form:
            clicked = request.form.get("choice")
            if clicked in selected:
                selected = [w for w in selected if w != clicked]
            elif len(selected) < 4:
                selected = selected + [clicked]
            session["connections_selected"] = selected
        # submit button
        elif "sub" in request.form and len(selected) == 4:
            solved = False
            correct = None
            for g in groups:
                match = True
                for w in selected:
                    if w not in g[1]:
                        match = False
                if match and len(g[1]) == 4:
                    solved = True
                    correct = g
            if solved:
                board = [w for w in board if w not in correct[1]]
                session["connections_board"] = board
                # remove solved group
                groups = [g for g in groups if g != correct]
                session["connections_groups"] = groups
                # add to solved groups
                solved_groups.append(correct)
                session["connections_solved_groups"] = solved_groups
                selected = []
                session["connections_selected"] = selected

                if len(session["connections_solved_groups"]) == 4:
                    session["connections_status"] = "win"
                    add_xp(session["user_id"], 30)
                    session["connections_xp"] = 30
            else:
                session["connections_mistakes"] -= 1
                msg = "Not a match"
                if session["connections_mistakes"] <= 0:
                    session["connections_status"] = "lose"
                    add_xp(session["user_id"], 5)
                    session["connections_xp"] = 5
                    session["connections_solved_groups"] = session["connections_all_groups"]
                    session["connections_board"] = []
            session["connections_selected"] = selected
    mistakes = session["connections_mistakes"]
    status = session["connections_status"]
    rows = [board[0:4], board[4:8], board[8:12], board[12:16]]
    xp_gain = session["connections_xp"]
    return render_template("connections.html", status = status, board = board, groups = groups, selected = selected, msg = msg, error = error,  mistakes = mistakes, solved_groups = solved_groups, rows = rows, xp_gain = xp_gain)


@app.route("/spellingBee", methods=["GET", "POST"])
def spellingBeePage():
    global word, goodWords, lttrs, score, submitted
    print(submitted)
    if not "user_id" in session:
        return redirect("/login")
    error = ""
    # lttrs = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    notLttrs = ["sub", "newL", "sub2", "delete"]
    if request.method == "POST":
        if (
            list(request.form.keys())[0] not in notLttrs
            and list(request.form.keys())[0]
        ):  # if submitted a letter
            # print(list(request.form.keys()))
            word += lttrs[int(list(request.form.keys())[0])]
        if (
            list(request.form.keys()) == ["sub"] and word
        ):  # if submitted a word -- not reloading
            truths = spellingBee.checkword(word, lttrs[0])
            used = word in goodWords
            if (
                truths[0] == True
                and truths[2] == False
                and not used
                and truths[3] == True
            ):
                goodWords += [word]
                score += len(word)
            elif truths[1] == False:
                error = "There was an error with the API"
            elif truths[0] == False:
                error = "Word does not exist"
            elif truths[2] == True:
                error = "Word is too short"
            elif truths[3] == False:
                error = "Does not have necessary letter"
            else:
                error = "Word already used"
            word = ""
        elif list(request.form.keys()) == ["newL"]:  # new letters
            lttrs = spellingBee.randNums()
            goodWords = []
            word = ""
            score = 0
        elif list(request.form.keys()) == ["delete"]:
            word = word[:-1]
        elif list(request.form.keys()) == ["sub2"]:  # submit score
            print(fetch("users", "user_id = ?", "xp", (session["user_id"],)))
            add_xp(session["user_id"], score)
            submitted += 1
            score = 0
            goodWords = []
            lttrs = spellingBee.randNums()
            word = ""
    return render_template(
        "spellingBee.html",
        letters=lttrs,
        w=word,
        error=error,
        words=goodWords,
        score=score,
        able=(submitted == 3),
    )


@app.route("/ingredients", methods=["GET", "POST"])
def ingredientsGuesserPage():
    if not "user_id" in session:
        return redirect("/login")

    word_input = ""
    if request.method == "POST":
        word_input = request.form.get("input_ing")
        print("word input: " + word_input)
    rand_ing = ingredients.random_ingredient()
    print("random ingredient: " + rand_ing)
    rand_meal = ingredients.random_meal(rand_ing)
    print("random meal id: " + str(rand_meal))
    while rand_meal == 0:
        rand_ing = ingredients.random_ingredient()
        rand_meal = ingredients.random_meal(rand_ing)
    meal_ing = ingredients.meal_ingredients(rand_meal)
    if word_input in meal_ing:
        print("correct")
    image_url = ingredients.meal_img(rand_meal)
    return render_template("ingredients.html", image_url=image_url)


def fetch(table, criteria, data, params=()):
    db = get_db()
    c = db.cursor()
    query = f"SELECT {data} FROM {table} WHERE {criteria}"
    c.execute(query, params)
    data = c.fetchall()
    db.close()
    return data


# <-------------------- CREATURES -------------------->


def hatch(s, l):
    user_id = session["user_id"]
    species = s
    level = l

    if species == "chicken":
        rarity = "common"
    elif species == "greenBird":
        rarity = "uncommon"
    db = get_db()
    c = db.cursor()
    c.execute(
        """INSERT INTO creatures (user_id, name, rarity, xp, level, species, status) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, species.capitalize(), rarity, 0, level, species, "hatched"),
    )
    db.commit()
    db.close()
    return True


# Flask
if __name__ == "__main__":
    app.debug = True
    app.run()
