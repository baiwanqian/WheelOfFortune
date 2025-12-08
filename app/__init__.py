import sqlite3
import random
from flask import Flask, render_template
from flask import session, request, redirect
import os
import requests

# Flask
app = Flask(__name__)
app.secret_key = 'bdzfgetdzhezt'

# SQLite
DB_FILE = "data.db"

# allows sqlite rows to be accessed like dictionaries instead of tuples
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# database creation
db = get_db()
c = db.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    xp INTEGER,
    level INTEGER)
    """);

c.execute("""
    CREATE TABLE IF NOT EXISTS creatures (
    creature_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    name TEXT,
    rarity TEXT,
    xp INTEGER,
    level INTEGER,
    image_path TEXT,
    status TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id))
    """);

db.commit()
db.close()

# HTML PAGES
# LANDING PAGE
@app.route('/', methods=["GET", "POST"])
def homepage():
    if not 'user_id' in session:
        return redirect("/login")
    return render_template("home.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        usernames = [row[0] for row in fetch("users", "TRUE", "username")]
        if not request.form['username'] in usernames:
                return render_template("login.html",error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>")
        elif request.form['password'] != fetch("users", "username = ?", "password", (request.form['username'],))[0][0]:
                return render_template("login.html",error="Wrong &nbsp username &nbsp or &nbsp password!<br><br>")
        else:
            session["user_id"] = fetch("users", "username = ?", "user_id", (request.form['username'],))[0][0]
    if 'user_id' in session:
        return redirect("/")
    session.clear()
    return render_template("login.html")


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop("user_id", None)
    return redirect("/login")


@app.route('/register', methods=["GET", "POST"])
def register():
    if 'user_id' in session:
        return redirect("/")
    if request.method == "POST":
        usernames = [row[0] for row in fetch("users", "TRUE", "username")]
        if request.form['username'] in usernames:
            return render_template("register.html", error="Username already taken, please try again! <br><br>")
        elif request.form['password'] != request.form['confirm']:
            return render_template("register.html", error="Passwords don't match! <br><br>")
        else:
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            c.execute("SELECT COUNT(*) FROM users")
            u_id = c.fetchall()[0][0]
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)",(u_id, request.form['username'], request.form['password'], 0, 0,))
            db.commit()
            c.execute("SELECT user_id FROM users WHERE username = ?", (request.form['username'],))
            session["user_id"] = c.fetchone()[0]
            db.close()
            return redirect("/")
    return render_template("register.html")


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect("/login")

    db = get_db()
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE user_id = ?", (session["user_id"],))
    user = c.fetchone()
    c.execute("SELECT * FROM creatures WHERE user_id = ?", (session["user_id"],))
    creatures = c.fetchall()

    db.close()

    return render_template(
        "profile.html",
        username = user["username"],
        xp = user["xp"],
        level = user["level"],
        creatures = creatures,
        background_img = bg_file
    )

headers = {'IDontKnowWhatTheNameIs' : 'WheelOfFortune'}

STUY_LAT = 40.7127
STUY_LON = -74.0061

def currentWeather():
    #try:
        #gets data at lat and lon coordinates
        endpoint = f'https://api.weather.gov/points/{STUY_LAT},{STUY_LON}'
        print(lat)
        print(lon)
        print(endpoint)
        response = requests.get(endpoint, headers = headers)
        data = response.json()

        #gets all links about at pt (hourly daily etc)
        links = data["forecastGridData"]
        print(links)

        #gets link relating to daily forecast at pt
        forecast_link = data["properties"]["forecast"]
        print(forecast_link)

        #retrieves forecast data at coordinates
        forecast_response = requests.get(forecast_link, headers = headers)
        forecast_data = forecast_response.json()
        print(forecast_data)

        #gets most recently updated forecast for next period (for example: Monday, Monday Night, Tuesday, etc.)
        forecast = forecast_data["properties"]["periods"][0]["shortForecast"]
        print(forecast)

        return forecast

def bg_file():
    basepath = './static/background_images'
    print(os.listdir(basepath))

    if "Sunny" in currentWeather() or "sunny" in currentWeather():
        basepath = './static/background_images/sunny_weather'
    if "Cloudy" in currentWeather() or "cloudy" in currentWeather():
        basepath = './static/background_images/cloudy_weather'
    if "Rainy" in currentWeather() or "rainy" in currentWeather():
        basepath = './static/background_images/rainy_weather'
    if "Snowy" in currentWeather() or "snowy" in currentWeather():
        basepath = './static/background_images/snowy_weather'

    image = random.choice(os.listdir(basepath))
    print(image)

    return image


# <-------------------- MINIGAMES -------------------->
@app.route('/wordle', methods=["GET", "POST"])
def wordlePage():
    if not 'user_id' in session:
        return redirect("/login")
    if request.method == "POST":
        #word_input =
        pass #temp placeholder so it runs)
    return render_template("wordle.html")

@app.route('/connections', methods=["GET", "POST"])
def connectionsPage():
    if not 'user_id' in session:
        return redirect("/login")
    if request.method == "POST":
        #word_input =
        pass #temp placeholder so it runs)
    return render_template("connections.html")

@app.route('/spelling', methods=["GET", "POST"])
def spellingBeePage():
    if not 'user_id' in session:
        return redirect("/login")
    if request.method == "POST":
        #word_input =
        pass #temp placeholder so it runs)
    return render_template("spelling.html")

@app.route('/ingredients', methods=["GET", "POST"])
def ingredientsGuesserPage():
    if not 'user_id' in session:
        return redirect("/login")
    if request.method == "POST":
        #word_input =
        pass #temp placeholder so it runs)
    return render_template("ingredients.html")

def fetch(table, criteria, data, params = ()):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = f"SELECT {data} FROM {table} WHERE {criteria}"
    c.execute(query, params)
    data = c.fetchall()
    db.commit()
    db.close()
    return data




# Flask
if __name__=='__main__':
    app.debug = True
    app.run()
