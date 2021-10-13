import requests
from urllib.parse import unquote
import base64
import json
from bs4 import BeautifulSoup
from flask_spotify_auth import getAuth, refreshAuth, getToken

#Add your client ID
CLIENT_ID = "6cf531e2a1bc4dc9a708b7bd443b5ea1"

#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = "373715f25ef8492980011ca4d20a8aba"

#Port and callback url can be changed or ledt to localhost:5000
PORT = "5000"
CALLBACK_URL = "http://localhost"

#Add needed scope from spotify user
SCOPE = "playlist-read-private,playlist-read-collaborative"
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "{}:{}/callback/".format(CALLBACK_URL, PORT), SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/callback/".format(CALLBACK_URL, PORT))
 
def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA


def getUserJSON(access_token):
        header = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://api.spotify.com/v1/me"
        res_json = requests.get(base_url, headers=header).json()
        username = res_json['id']
        return username

def getUserPlaylists(access_token, username):
        header = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://api.spotify.com/v1/users/{username}/playlists"
        res_json = requests.get(base_url, headers=header).json()
        return res_json

    

