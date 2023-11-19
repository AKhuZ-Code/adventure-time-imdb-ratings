# Used as inspiration:  https://abdulrwahab.medium.com/how-to-build-a-python-web-scraper-to-capture-imdb-top-100-movies-908bf9b6bc19

# Import required modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

### Set for loop to get data across all seasons

# Get all season numbers + unknown
seasons_list = list(range(1,11))
seasons_list = list(map(str, seasons_list))
seasons_list.append('Unknown')

# Create a URL for each of the seasons - and put these URLs into a list
imdb_url_base = 'https://www.imdb.com/title/tt1305826/episodes/?season='
imdb_url_list = []
for item in seasons_list:
     imdb_url_list.append(imdb_url_base+item)

### Initialise a txt file
open('adventuretime.txt', 'w').close()

### Define columns of the dataframe
episode_full = []
description_full = []
rating_full = []
number_votes_full = []
air_date_full = []

### Start the for loop

for item in imdb_url_list:

    ### Download the html file from the links
    imdb_url = item
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    , "Accept-Language": "en-US, en;q=0.5"}
    res = requests.get(imdb_url, headers=headers)
    res.raise_for_status()

    ### Save the html data into the txt file
    testfile = open('adventuretimetest.txt', 'wb')
    for chunk in res.iter_content(100000):
        testfile.write(chunk)
    testfile.close()

    ### Parse the HTML data
    testfile = open('adventuretimetest.txt')

    ### Create BS object
    adventuretime_soup = BeautifulSoup(testfile, "html.parser")

    ### Set up variables to collect raw html data, for each season
    episode_html = adventuretime_soup.find_all('div', {"class": "ipc-title__text"})
    description_html = adventuretime_soup.find_all('div', {"class": "ipc-html-content-inner-div"})
    rating_html = adventuretime_soup.find_all('span', {"class": "ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating"})
    number_votes_html = adventuretime_soup.find_all('span', {"class": "ipc-rating-star--voteCount"})
    air_date_html = adventuretime_soup.find_all('span', {"class": "sc-9115db22-10 fyHWhz"})

    ### Set up variables to collect text, for each season
    episode = []
    for item in episode_html:
        episode.append(item.getText())

    description = []
    for item in description_html:
        description.append(item.getText())

    rating = []
    for item in rating_html:
        rating.append(item.get('aria-label'))

    number_votes = []
    for item in number_votes_html:
        number_votes.append(item.getText())

    air_date = []
    for item in air_date_html:
        air_date.append(item.getText())

    ### Extend current season's data to master lists. Use master list later when creating the dataframe.
    episode_full.extend(episode)
    description_full.extend(description)
    rating_full.extend(rating)
    number_votes_full.extend(number_votes)
    air_date_full.extend(air_date)

### Check length of all arrays
# print(len(episode_full))
# print(len(description_full))
# print(len(rating_full))
# print(len(number_votes_full))
# print(len(air_date_full))

### Create output dataframe
df = pd.DataFrame({
    'episode': episode_full,
    'description': description_full,
    'rating': rating_full,
    'number of votes': number_votes_full,
    'air date': air_date_full
})

### Format/clean data entries
pattern_rating = r'IMDb rating: (.*)'
pattern_number_votes = r'\xa0\((.*?)\)'

df['episode'] = df['episode'].str.strip('"')
df['description'] = df['description'].str.strip('"')
df['rating'] = df['rating'].str.extract(pattern_rating)
df['number of votes'] = df['number of votes'].str.extract(pattern_number_votes)

### Output data
csv_file_path = 'adventuretimedata.csv'
df.to_csv(csv_file_path, index=False)

print(f'DataFrame has been successfully saved to {csv_file_path}')

