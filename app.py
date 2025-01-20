from flask import Flask, redirect, request, jsonify, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

app = Flask(__name__)

CLIENT_ID = "CLIENT_ID giriniz"
CLIENT_SECRET = "CLIENT_SECRET giriniz"
REDIRECT_URI = "http://localhost:5000/callback"
SCOPE = "user-top-read playlist-read-private user-read-private user-read-email"

#scope kısmınıda sonrasında top100 e göre düzenleyeceğiz
#not olarak şuna dikkat! normal spotify hesabınıza tarayıcıda girmiş olun, birde kullanıcıyı soldaki dosyalarda vermiş olduğum görseldeki gibi sisteme eklemesini yapınız sonrasında marşı verin gitsin :)

# SpotifyOAuth nesnesini oluştur
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=".spotifycache"
)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    token_info = auth_manager.get_access_token(code)
    
    if token_info:
        sp = spotipy.Spotify(auth_manager=auth_manager)
        try:
            top_tracks = sp.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')
            track_list = []
            
            for track in top_tracks['items']:
                track_info = {
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'popularity': track['popularity']
                }
                track_list.append(track_info)
                
            return render_template('results.html', tracks=track_list)
        except Exception as e:
            return f"Hata oluştu: {str(e)}"
    
    return "Token alınamadı"

if __name__ == "__main__":
    app.run(debug=True, port=5000)