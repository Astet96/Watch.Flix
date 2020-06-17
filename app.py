# Main webapp logic is here
import os
import sqlite3
from datetime import datetime
import requests
from flask import Flask, jsonify, redirect, render_template, request, url_for
from qry_cnstrctr import qry, rand_qry, t_name
from img import get_poster


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

cdir = os.getcwd()
static_dir = cdir + r'\\static'
tmp_dir = static_dir + r'\\tmp'
db_dir = cdir + r'\\db'
os.chdir(db_dir)

conn = sqlite3.connect('IM.db')
crsr = conn.cursor()

row = sqlite3.connect('rows.db')
pop = row.cursor()

pop.execute("SELECT genre FROM genre")
tmp_genre = pop.fetchall()
genre = [None] * len(tmp_genre)
for i in range(len(tmp_genre)):
    genre[i] = tmp_genre[i][0]
del tmp_genre

pop.execute("SELECT * FROM actor")
tmp_actor = pop.fetchall()
actor = [None] * len(tmp_actor)
for i in range(len(tmp_actor)):
    actor[i] = tmp_actor[i][0]
del tmp_actor

pop.execute("SELECT * FROM director")
tmp_director = pop.fetchall()
director = [None] * len(tmp_director)
for i in range(len(tmp_director)):
    director[i] = tmp_director[i][0]
del tmp_director

pop.execute("SELECT * FROM producer")
tmp_producer = pop.fetchall()
producer = [None] * len(tmp_producer)
for i in range(len(tmp_producer)):
    producer[i] = tmp_producer[i][0]
del tmp_producer

pop.execute("SELECT * FROM country")
tmp_country = pop.fetchall()
country = [None] * len(tmp_country)
for i in range(len(tmp_country)):
    country[i] = tmp_country[i][0]
del tmp_country
row.close()

error = [None] *3
movie = None
history = [None] *10
name_history = [None] *10
ind = 10
ind2 = 10

def incr(movie):
    global ind
    ind -= 1
    if ind < 0:
        for i in range(9, 0, -1):
            history[i] = history[i-1]
        ind = 0
    history[ind] = movie

def incr2(name):
    global ind2
    ind2 -= 1
    if ind2 < 0:
        for i in range(9, 0, -1):
            name_history[i] = name_history[i-1]
        ind2 = 0
    name_history[ind2] = name

def film(tconst):
    try:
        cnn = sqlite3.connect('IM.db')
        crs = cnn.cursor()
        sel = ("SELECT primaryTitle FROM title_basics WHERE tconst ='{}'" .format(tconst))
        crs.execute(sel)
        tmp_name = crs.fetchone()
        name = t_name(tmp_name)
        cnn.close()
        return name
    except:
        return ""


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        for i in range(len(error)):
            error[i] = None
        crit = [None] * 8
        crit[0] = request.form.get("type")
        crit[1] = request.form.get("year")
        crit[2] = request.form.get("genre")
        crit[3] = request.form.get("rating")
        crit[4] = request.form.get("actor")
        if crit[4] != "" and not crit[4] in actor:
            error[0] = "Unrecognised Actor!"
        crit[5] = request.form.get("director")
        if crit[5] != "" and not crit[5] in director:
            error[1] = "Unrecognised Director!"
        crit[6] = request.form.get("producer")
        if crit[6] != "" and not crit[6] in producer:
            error[2] = "Unrecognised Producer!"
        crit[7] = request.form.get("region")


        for i in range(len(error)):
            if error[i] != None:
                return render_template("index.html", error=error, genre=genre, country=country)
        
        movie = qry(crit)
        return redirect(url_for("result", movie=movie))

    else:
        return render_template("index.html", error=error, genre=genre, country=country)

@app.route("/result/<movie>")
def result(movie):
    try:
        time = datetime.now().strftime("%f%M%S")
        get_poster(movie, time)
        pstr_f = r'poster' + str(time) + r'.jpg'
        pstr = r'tmp/' + pstr_f
        url = url_for('static', filename=pstr)
        name = film(movie)
        incr(movie)
        incr2(name)
        return render_template("result.html", url=url, time=time, movie=movie, name=name)
    except:
        os.chdir("..")
        os.chdir("..")
        os.chdir(db_dir)
        return render_template("not_found.html")

@app.route("/random", methods = ["GET", "POST"])
def random():
    if request.method == "POST":
        movie = rand_qry()
        return redirect(url_for("result", movie=movie))
    else:
        return render_template("random.html")

@app.route("/history")
def hstr():
    return render_template("history.html", history=history, name_history=name_history, ind=ind)

@app.route("/about")
def about():
    return render_template("about.html")