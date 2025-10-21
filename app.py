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
        temp = {"title":song["name"], "rating":-1}
        retList.append(temp)
    return retList

@app.route("/")
def home():
    return render_template("index.html", failed = False)

@app.route("/start", methods=["POST"])
def start():
    artist = request.form["artist"]
    album = request.form["album"]
    session["artist"] = artist
    session["album"] = album
    session["songIndex"] = 0
    session["songList"] = getSongs(artist,album)
    session["categories"]={"great":[], "mid":[], "bad":[]}

    if not session["songList"]:
        return render_template("index.html", failed=True)
    
    return render_template("rank.html", title=session["songList"][session["songIndex"]]["title"])

@app.route("/rank", methods=["POST"])
def rank():
    choice = request.form["choice"]
    currSong = session["songList"][session["songIndex"]]
    currSong["category"]=choice
    session["categories"][choice].append(currSong)
    session["songIndex"]+=1
    if session["songIndex"]>=len(session["songList"]):
        return render_template("sort.html", categories = session["categories"])
    return render_template("rank.html", title=session["songList"][session["songIndex"]]["title"])
'''
    if(len(session["categories"][choice])==0):
        session["categories"][choice].append(currSong)
        session["songIndex"]+=1
        currSong = session["songList"][session["songIndex"]]
        return render_template("rank.html", title = currSong["title"])
    else:
        session["min"]=0
        session["max"]=len(session["categories"][choice])
        session["midpoint"]=(int)((session["min"]+session["max"])/2)
        session["currCat"]=session["categories"][choice]
         
        return render_template("sort.html", current=session["songList"][session["songIndex"]]["title"], middle=session["currCat"][session["midpoint"]]["title"])
    
    if session["songIndex"]==len(session["songList"]):
        return render_template("final.html")
    
    return render_template("rank.html", title = session["songList"][session["songIndex"]]["title"])

@app.route("/sort", methods=["POST"])
def sort():
    choice = request.form["pick"]
    if(choice=="curr"):
        session["max"]=session["midpoint"]-1
        session["midpoint"]=(int)((session["max"]+session["min"])/2)
        if(session["min"]>session["max"]):
            session["currCat"].insert(session["min"], session["songList"][session["songIndex"]]["title"])
            session["songIndex"] += 1
            return render_template("rank.html", title=session["songList"][session["songIndex"]]["title"])
        return render_template("sort.html", current=session["songList"][session["songIndex"]]["title"], middle=session["currCat"][session["midpoint"]]["title"])
'''
if __name__ == "__main__":
    app.run(debug=True)