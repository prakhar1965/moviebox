import csv
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

def func(row):
    return str(row['movie_title']).rstrip()
i = 0
with open('movie_poster.csv', 'a', newline='') as out_csv:
    data = pd.read_csv('movie_metadata.csv', usecols=['movie_title'])
    print(data.loc[458])
    # for link in data['movie_imdb_link']:
    #     movie_url = link
    #     domain = 'http://www.imdb.com'
    #     with urllib.request.urlopen(movie_url) as response:
    #         html = response.read()
    #         soup = BeautifulSoup(html, 'html.parser')
    #         print(i)
    #         i += 1
    #         try:
    #             image_url = soup.find('div', class_='poster').a.img['src']
    #             print(image_url)
    #
    #
    #             with open('movie_poster.csv', 'a', newline='') as out_csv:
    #                 writer = csv.writer(out_csv, delimiter=',')
    #                 writer.writerow([image_url])
    #         # Ignore cases where no poster image is present
    #         except AttributeError:
    #             pass