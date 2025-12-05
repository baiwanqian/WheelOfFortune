
import sqlite3
import random
from flask import Flask, render_template
from flask import session, request, redirect

# Flask
app = Flask(__name__)
app.secret_key = 'bdzfgetdzhezt'

# SQLite
DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, exp INTEGER, level INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS creatures(creature_id creature_id, user_id INTEGER, name TEXT, rarity TEXT, exp INTEGER, level INTEGER, image_path TEXT, status TEXT)")

db.commit()
db.close()


# HTML PAGES
# LANDING PAGE
@app.route('/', methods=["GET", "POST"])
def homepage():
    if 'user_id' not in session:
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
            session["user_id"] = fetch("users", "username = ?", "rowid", (request.form['username'],))[0]
    if 'user_id' in session:
        return redirect("/")
    session.clear()
    return render_template("login.html")


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop("u_rowid", None)
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
            db.close()
    return render_template("register.html")




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

