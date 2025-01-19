from flask import Flask, redirect, request, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import requests
import os

app = Flask(__name__)

# Spotify API Credentials
CLIENT_ID = "192f887a420c413ea18270fec94300ec"
CLIENT_SECRET = "ba6deb9f7d944260bcf3799dc79a9d6d"
REDIRECT_URI = "http://localhost:5000/callback"

# Spotify Auth URL
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Authorization Scope
SCOPE = "playlist-read-private"

@app.route("/")
def login():
    # Construct the Spotify authorization URL
    auth_url = f"{SPOTIFY_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    # Step 1: Get the authorization code from the query parameters
    code = request.args.get("code")

    if not code:
        return jsonify({"error": "Authorization code not found."}), 400

    # Step 2: Exchange the authorization code for an access token
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    # Send the request to Spotify's token endpoint
    response = requests.post(SPOTIFY_TOKEN_URL, data=token_data)

    # Step 3: Check if the response is successful
    if response.status_code != 200:
        return jsonify({"error": "Failed to get access token.", "details": response.json()}), response.status_code

    # Step 4: Extract the access token from the response
    access_token = response.json().get("access_token")
    refresh_token = response.json().get("refresh_token")

    # Log the access token and refresh token (you can store them for future use)
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)

    # Step 5: Return the access token and refresh token as JSON
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
