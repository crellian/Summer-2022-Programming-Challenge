import requests
from bs4 import BeautifulSoup
import re
import json

#obtain a list of urls of news articles
site_url = 'https://www.aljazeera.com'
news_url = '/where/mozambique'

response = requests.get(site_url + news_url)
soup = BeautifulSoup(response.content, 'html.parser')

urls = []
blocks = soup.find_all('article')
for b in blocks:
    links = b.find_all('a', class_='u-clickable-card__link')
    for l in links:
        if l['href'].startswith('/program'):
            continue
        urls.append(site_url + l['href'])

urls = urls[:10]
response.close()

#store articles in a JSON file
news = []
for url in urls:
    data = {}
    data['url'] = url
    res_article = requests.get(url)
    sp_article = BeautifulSoup(res_article.content, 'html.parser')
    title = sp_article.h1.string 
    subhead = sp_article.find('p', class_='article__subhead css-1wt8oh6')
    if subhead:
        data['subhead'] = subhead.string
    data['title'] = title
    
    texts = sp_article.find_all('p')
    article = []
    for text in texts:
        text_plain = re.sub(r'<a .*\">', '', str(text))
        text_plain = re.sub(r'<p class=\"site-footer.*</p>', '', text_plain)
        text_plain = re.sub(r'<p dir=.*</p>', '', text_plain)
        text_plain = re.sub(r'<p .*\">', '', text_plain)
        text_plain = re.sub(r'<p>—.*</a></p>', '', text_plain)
        text_plain = re.sub(r'<script.*script>', '', text_plain)
        text_plain = re.sub(r'<em>.*</em>', '', text_plain)
        paragraphs = text_plain.replace('<p>', '') \
                               .replace('</p>', '') \
                               .replace('<strong>', '') \
                               .replace('</strong>', '') \
                               .replace('</a>', '') \
                               .replace('<br/>', '\n') \
                               .split('\n')
        paragraphs = [x for x in paragraphs if x and x!=' ']
        article += paragraphs
   
    data['article'] = article   
    news.append(data)

with open('../news.json', 'w') as f:
    json.dump(news, f, indent=4)
    

