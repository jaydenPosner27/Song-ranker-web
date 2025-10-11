import requests
import string


API_KEY = "ad1178859688fbab3634d9904e6c3273"

def normalize(title):
    normalized = str.maketrans('', '', string.punctuation + " ")
    return title.translate(normalized).lower()

def getSongs(artist, album):
    url = "https://ws.audioscrobbler.com/2.0/"
    param = {"method":"album.getinfo", "api_key":API_KEY, "artist":artist, "album":album, "format":"json"}
    data = requests.get(url, params=param).json()
    songData = data["album"]["tracks"]["track"]
    retList = []
    for song in songData:
        retList.append(song["name"])
    return retList


def compare(allSongs, rankedSongs):
    print("For the following ranking, you will give each song a ranking of either great, mid, or bad. You may also skip songs by entering the word skip. All capitalization, spaces and punctuation can be disregarded")

    for songs in allSongs:
        min = 0
        category = input("Would you say " + songs + " is great, mid, or bad? ").lower()
        if category == "skip":
            continue
        while category not in rankedSongs:
            category = input("enter a valid answer ").lower()
        max = len(rankedSongs[category])-1
        if max == -1:
            rankedSongs[category].append(songs)
            continue
        i=int(max/2)
        while(True):
            choice = input(songs + " or " + rankedSongs[category][i] + "? ")
            if normalize(choice) == normalize(songs):
                max = i -1
                #print(str(min) + " " + str(max) + " " + str(i))
            elif normalize(choice) == normalize(rankedSongs[category][i]):
                min = i + 1
                #print(str(min) + " " + str(max) + " " + str(i))
            else:
                print("enter a valid answer")
            if min>max:
              rankedSongs[category].insert(min,songs)
              break
            i = int((min+max)/2)
    
def sort(sortedList):
    for buckets in sortedList:
        i = 0
        weight = 32/len(sortedList[buckets])
        match buckets:
            case "great":
                max = 100
            case "mid":
                max = 67
            case "bad":
                max = 33
            case "scores":
                return
        for songs in sortedList[buckets]:
            sortedList["scores"].append(int(max-weight*i))
            i= i + 1
            

artistName = input("You will enter the name of a music artist, and one of their albums, then rank the songs. First, enter in the name of the artist whose album you want to rank\n")
albumName=input("Now enter the name of the album\n")
rankedList = {
    "great":[], "mid":[], "bad":[], "scores":[]
}
songList = getSongs(artistName, albumName)
compare(songList,rankedList)
sort(rankedList)
i = 0

for songs in rankedList["great"]:
    print(str(songs) + " " + str(rankedList["scores"][i]))
    i = i + 1
for songs in rankedList["mid"]:
    print(str(songs) + " " + str(rankedList["scores"][i]))
    i = i + 1
for songs in rankedList["bad"]:
    print(str(songs) + " " + str(rankedList["scores"][i]))
    i = i + 1
    
