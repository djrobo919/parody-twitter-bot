import os
import requests
from requests_oauthlib import OAuth1

def post_tweet(text):
    url = "https://api.x.com/2/tweets"

    auth = OAuth1(
        os.environ["X_API_KEY"],
        os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"],
        os.environ["X_ACCESS_SECRET"],
    )

    payload = {"text": text}

    response = requests.post(url, json=payload, auth=auth)

    print("X API status code:", response.status_code)
    print("X API response:", response.text)

    if response.status_code not in (200, 201):
        raise Exception("Tweet was not posted")

    return response.json()
