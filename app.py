from flask import Flask, render_template, request
from flask import session
import requests
import string

app = Flask(__name__)
API_KEY = "ad1178859688fbab3634d9904e6c3273"
app.secret_key = "THIS IS MY RANDOM KEEEEYYYY"

def getSongs(artist, album):
    url = "https://ws.audioscrobbler.com/2.0/"
    param = {"method":"album.getinfo", "api_key":API_KEY, "artist":artist, "album":album, "format":"json"}
    data = requests.get(url, params=param).json()
    try:
        songData = data["album"]["tracks"]["track"]
    except:
        return []
    retList = []
    for song in songData:
        temp = {"title":song["name"], "category":"", "rating":-1}
        retList.append(temp)
    return retList

@app.route("/")
def home():
    return render_template("index.html", failed = False)

@app.route("/start", methods=["POST"])
def songs():
    artist = request.form["artist"]
    album = request.form["album"]
    session["artist"] = artist
    session["album"] = album
    session["songList"] = getSongs(artist,album)
    session["songIndex"] = 0
    print(len(session["songList"]))
    if not session["songList"]:
        return render_template("index.html", failed=True)
    return render_template("rank.html", title = session["songList"][session["songIndex"]]["title"])

@app.route("/rank", methods=["POST"])
def rank():
    print(session["songIndex"])
    session["songList"][session["songIndex"]]["category"]=request.form["choice"]
    session["songIndex"] += 1
    if session["songIndex"]==len(session["songList"]):
        return render_template("final.html")
    return render_template("rank.html", title = session["songList"][session["songIndex"]]["title"])


if __name__ == "__main__":
    app.run(debug=True)