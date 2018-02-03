import json
import requests
from .credentials import API_key

api_url = "https://www.googleapis.com/urlshortener/v1/url?key=" + API_key

def get_shortenUrl(longUrl):
    r = requests.post(api_url, headers={"Content-Type": "application/json"}, data=json.dumps({"longUrl": longUrl}))
    return r.json()['id']