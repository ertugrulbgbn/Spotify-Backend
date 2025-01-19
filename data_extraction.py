import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify

# 🎵 Spotify API Kimlik Bilgileri
CLIENT_ID = "192f887a420c413ea18270fec94300ec"  # Gerçek client_id'nizi buraya yazın
CLIENT_SECRET = "ba6deb9f7d944260bcf3799dc79a9d6d"  # Gerçek client_secret'inizi buraya yazın
REDIRECT_URI = "http://localhost:5001/callback"  # Uygulamanın geri dönmesi gereken URL
SCOPE = "user-top-read"  # Erişim izni

# 📌 Spotipy Yetkilendirme
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

def get_access_token():
    """Erişim token'ını almak için kullanıcıyı Spotify'a yönlendirir."""
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )
    auth_url = auth_manager.get_authorize_url()
    print(f"Spotify'a giriş yapmak için şu URL'yi ziyaret edin: {auth_url}")
    
    # Kullanıcıdan gelen kodu al (bu URL'deki kodu alarak)
    code = input("Authorization code'u girin: ")  # Kullanıcı bu kodu URL'den alacak
    token_info = auth_manager.get_access_token(code)
    return token_info['access_token']

def get_top_tracks(access_token):
    """ Kullanıcının en çok dinlediği 50 şarkıyı çeker ve analiz verilerini alır. """
    sp = spotipy.Spotify(auth=access_token)  # Token ile oturum aç
    top_tracks = sp.current_user_top_tracks(time_range='long_term', limit=50)
    
    track_data = []

    for track in top_tracks['items']:
        track_id = track['id']
        track_info = {
            'track_id': track_id,
            'track_name': track['name'],
            'artist': track['artists'][0]['name'],
            'popularity': track['popularity'],
            'album': track['album']['name'],
            'release_date': track['album']['release_date']
        }

        # 🎼 Şarkının ses analiz verilerini çek
        audio_features = sp.audio_features([track_id])[0]

        if audio_features:  # Eğer ses verileri varsa ekle
            track_info.update({
                'danceability': audio_features.get('danceability', 0.0),
                'energy': audio_features.get('energy', 0.0),
                'tempo': audio_features.get('tempo', 0.0),
                'acousticness': audio_features.get('acousticness', 0.0),
                'valence': audio_features.get('valence', 0.0),
            })
        
        track_data.append(track_info)

    return track_data

if __name__ == "__main__":
    # Erişim token'ını al
    access_token = get_access_token()

    # Kullanıcının en çok dinlediği şarkıları al
    tracks = get_top_tracks(access_token)

    # 🎵 Sonuçları ekrana yazdır
    for i, track in enumerate(tracks, start=1):
        print(f"{i}. {track['track_name']} - {track['artist']} ({track['album']})")
        print(f"   🎵 Tempo: {track['tempo']} | 🕺 Danceability: {track['danceability']} | 🔥 Energy: {track['energy']}\n")

if __name__ == "__main__":
    app.run(debug=True, port=5001)