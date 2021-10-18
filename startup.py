import requests
import json
from flask_spotify_auth import getAuth, refreshAuth, getToken
import random

#Add your client ID
CLIENT_ID = "6cf531e2a1bc4dc9a708b7bd443b5ea1"

#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = "373715f25ef8492980011ca4d20a8aba"

#Port and callback url can be changed or ledt to localhost:5000
PORT = "5000"
CALLBACK_URL = "http://localhost"

#Add needed scope from spotify user
SCOPE = "playlist-read-private,playlist-read-collaborative, playlist-modify-public, playlist-modify-private"
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "http://spotifycouplesapp.herokuapp.com/callback/", SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "http://spotifycouplesapp.herokuapp.com/callback/")
 
def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA


def getUserJSON(access_token):
        user = []
        header = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://api.spotify.com/v1/me"
        res_json = requests.get(base_url, headers=header).json()
        user.append(res_json['id'])
        user.append(res_json['display_name'])
        user.append(res_json['images'][0]['url'])
        return user

def getFriendJSON(access_token, friendID):
        user = []
        header = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://api.spotify.com/v1/users/{friendID}"
        res_json = requests.get(base_url, headers=header).json()
        print(res_json)
        if("error" in res_json):
            return("none")
        user.append(res_json['id'])
        user.append(res_json['display_name'])
        user.append(res_json['images'][0]['url'])
        return user


def getUserPlaylists(access_token, username):
        header = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://api.spotify.com/v1/users/{username}/playlists?limit=50"
        res_json = requests.get(base_url, headers=header).json()
        return res_json
    
def getPlaylistItems(access_token, playid):
        header = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://api.spotify.com/v1/playlists/{playid}/tracks"
        res_json = requests.get(base_url, headers=header).json()
        return res_json

def getUserOwnedPlaylists(playlists, userid):
        userPlaylists = []
        PlaylistIDs = []
        PlaylistNames = []
        for i in range(len(playlists["items"])):
            if(playlists["items"][i]["owner"]["id"] == userid and playlists["items"][i]["tracks"]["total"] > 0):
                PlaylistIDs.append(playlists["items"][i]["id"])
                PlaylistNames.append(playlists["items"][i]["name"])
            if(playlists["items"][i]["tracks"]["total"] == 0):
               print(playlists["items"][i]["name"])
        userPlaylists.append(PlaylistIDs)
        userPlaylists.append(PlaylistNames)
        return userPlaylists

def getRandomTrack(randomPlaylist, access_token):
        randomTrack = []
        randomTrackName = []
        randomTrackArtist = []
        randomTrackID = []
        for i in range(len(randomPlaylist[0])):
            tracks = getPlaylistItems(access_token, randomPlaylist[0][i])
            limit = len(tracks["items"])
            random_track = random.randint(0, limit-1)
            trackname = tracks["items"][random_track]["track"]["name"]
            artistname = tracks["items"][random_track]["track"]["album"]["artists"][0]["name"]
            trackid = tracks["items"][random_track]["track"]["id"]
            randomTrackName.append(trackname)
            randomTrackArtist.append(artistname)
            randomTrackID.append(trackid)
        randomTrack.append(randomTrackName)
        randomTrack.append(randomTrackArtist)
        randomTrack.append(randomTrackID)
        return randomTrack
                       
def getRandomPlaylists(userPlaylists, randNums, userimage):
        playlistInfo = []
        PlaylistIDs = []
        PlaylistNames = []

        for i in range(len(randNums)):
            PlaylistIDs.append(userPlaylists[0][randNums[i]])
            PlaylistNames.append(userPlaylists[1][randNums[i]])

        playlistInfo.append(PlaylistIDs)
        playlistInfo.append(PlaylistNames)
        playlistInfo.append(userimage)
        return playlistInfo

def getRandomNumberList(n, length):
        randNums = []
        for i in range(n):
            randNums.append(random.randint(0, length-1))
        return randNums

def generateCombinedList(playlist1, playlist2, randomPlaylist, randomFriendPlaylist, user, friend):
        combinedList = []
        for i in range(len(playlist1[0])):
            track1 = []
            track1.append(playlist1[0][i])
            track1.append(playlist1[1][i])       
            track1.append(playlist1[2][i])
            track1.append(randomPlaylist[1][i])
            track1.append(user)
            track1.append(randomPlaylist[2])
            track2 = []
            track2.append(playlist2[0][i])
            track2.append(playlist2[1][i])       
            track2.append(playlist2[2][i])
            track2.append(randomFriendPlaylist[1][i])
            track2.append(friend)
            track2.append(randomFriendPlaylist[2])
            combinedList.append(track1)
            combinedList.append(track2)
        return combinedList

def getIDarray(tracks):
        idArray = []
        for i in range(len(tracks)):
            idArray.append(tracks[i][2])
        return idArray
    
def createPlaylist(access_token, userid, username, friendname):
        header = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://api.spotify.com/v1/users/{userid}/playlists"
        name = f"{username} and {friendname}\'s Playlist"
        description = f"{username} and {friendname}\'s playlist created on http://spotifycouplesapp.herokuapp.com"
        public = "true"
        jsonData = {}
        jsonData["name"] = name
        jsonData["description"] = description
        jsonData["public"] = public
        playlistJson = json.dumps(jsonData)
        res_json = requests.post(base_url, data = playlistJson, headers=header).json()
        return res_json

def addPlaylistItems(access_token, playlist_id, idArray):
    ids = idArray.split(", ")
    header = {"Authorization": f"Bearer {access_token}"}
    for i in range(len(ids)):
        trackid = ids[i]
        trackid = trackid.replace("'",'')
        trackid = trackid.replace("[",'')
        trackid = trackid.replace("]",'')
        base_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris=spotify%3Atrack%3A{trackid}"
        res_json = requests.post(base_url, headers=header).json()
