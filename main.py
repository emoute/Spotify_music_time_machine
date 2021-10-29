from bs4 import BeautifulSoup
from datetime import datetime
import requests
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth

app_id = os.environ.get('APP_CLIENT_ID')
app_secret = os.environ.get('APP_CLIENT_SECRET')
redirect_uri = os.environ.get('APP_REDIRECT_URI')
current_year = datetime.now().year

# Check input for the errors
while True:
    try:
        chosen_year = int(input('Billboard list from which year you would like to choose (YYYY):'))
    except ValueError:
        print('Input year with numbers.\n')
        continue
    else:
        if chosen_year and 1980 <= chosen_year < current_year:
            break
        else:
            print('Retype year with numbers in a suggested variant - YYYY\n')
            continue

# Scrapping Billboard site to get all the artists and their track by the chosen year
bb_web_page = requests.get(url=f'https://www.billboard.com/charts/year-end/{chosen_year}/hot-100-songs').text
soup = BeautifulSoup(bb_web_page, 'html.parser')
artists = [artist.getText().replace('\n', '') for artist in soup.find_all('div', 'ye-chart-item__artist')]
tracks = [track.getText().replace('\n', '') for track in soup.find_all('div', 'ye-chart-item__title')]

# Initialize Spotify connection
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=app_id,
                                               client_secret=app_secret,
                                               redirect_uri='http://example.com',
                                               scope='playlist-modify-private',
                                               cache_path='token.txt'))
user_id = sp.current_user()["id"]
track_uris = []

# Add uri (id) of each track into the list
for track in tracks:
    result = sp.search(q=f'track:{track} year:{chosen_year}', type='track')
    try:
        uri = result['tracks']['items'][0]['uri']
        track_uris.append(uri)
    except IndexError:
        print(f'{track} doesn\'t exist in Spotify. Skip...')

# Creating playlist
playlist_id = sp.user_playlist_create(
    user_id,
    f'{chosen_year} year-end Billboard 100',
    public=False,
    collaborative=False,
    description=f'Playlist with songs from Year-end Billboard Top 100 by {chosen_year}.'
)['id']

# Filling playlist with songs
sp.playlist_add_items(playlist_id, track_uris, position=None)