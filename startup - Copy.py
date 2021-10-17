import requests
from urllib.parse import unquote
import base64
import json
from bs4 import BeautifulSoup

def getAccessToken():
    return TOKEN_DATA

   def get_song_json():
        header = {"Authorization": f"Bearer BQCZJWLX5Ci1gi3x0vXpYD2zl66F3cmcgDmkSG3PI3jE1ODM3NkP7CV6S7UN1EGbtgIxlUlZ6HGWn9vTBhjavblWJbUcHztaxfVFpEUEJGpeSbtU1OayECm9RGpWjjOeHRgoexvgsjhviXSVF"}
        base_url = f"https://api.spotify.com/v1/tracks/6PNvv1dmDbOWrAYwEcuKBX"
        res_json = requests.get(base_url, headers=header).json()

        return res_json
    

