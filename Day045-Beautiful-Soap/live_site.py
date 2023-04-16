from bs4 import BeautifulSoup
import pandas as pd
import requests

ENDPOINT = "https://news.ycombinator.com/"

response = requests.get(url=f"{ENDPOINT}/news")
response.raise_for_status()

site_data = response.text

soup = BeautifulSoup(site_data, 'html.parser')

recent_news = soup.find_all('span', class_='titleline')
recent_votes = soup.find_all('span', class_='score')

articles = []
for i, (news, vote) in enumerate(zip(recent_news, recent_votes)):
    article = news.a.text
    link = news.a.get('href')
    score = vote.text

    articles.append({'article': article, 'link': link, 'score': int(score.split(' ')[0])})

pd.set_option('display.max_colwidth', 0, 'display.width', 0)

df = pd.DataFrame(data=articles)
df.sort_values(by='score', axis=0, inplace=True, ascending=False)
df = df[['score', 'article', 'link']]
print(df)
