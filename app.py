from flask import Flask, render_template, request
import requests
import string

app = Flask(__name__)
API_KEY = "ad1178859688fbab3634d9904e6c3273"

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
        retList.append(song["name"])
    return retList

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/songs", methods=["POST"])
def songs():
    artist = request.form["artist"]
    album = request.form["album"]
    song_list = getSongs(artist,album)


if __name__ == "__main__":
    app.run(debug=True)