from bs4 import BeautifulSoup
from datetime import datetime
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

current_year = datetime.now().year

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

bb_web_page = requests.get(url=f'https://www.billboard.com/charts/year-end/{chosen_year}/hot-100-songs').text
soup = BeautifulSoup(bb_web_page, 'html.parser')
artists = [artist.getText().replace('\n', '') for artist in soup.find_all('div', 'ye-chart-item__artist')]
titles = [title.getText().replace('\n', '') for title in soup.find_all('div', 'ye-chart-item__title')]
artist_title_song = list(zip(artists, titles))

