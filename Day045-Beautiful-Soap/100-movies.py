import requests
from bs4 import BeautifulSoup

URL = 'https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/'

response = requests.get(url=URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

elements = soup.select(".article-title-description__text .title")

movies = [element.text+"\n" for element in elements[::-1]]

with open('movies.txt', 'w', encoding='utf-8') as f: f.writelines(movies)
