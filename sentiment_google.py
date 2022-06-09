import os
from google.cloud import language_v1
from tqdm import tqdm
import plotly.express as px
import chardet
import json
import re
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credential/japanese-ocr-337002-9b078adb6791.json'

def isEnglish(l):
    for d in l:
        title = re.sub(r'[\u2000-\u206F]', '', d['title'])
        la = chardet.detect(title.encode('ascii'))['encoding']
        if la != 'ascii':
            return False
    return True

def countSentence(l):
    count = 0
    for d in l:
        count += len(d['article'])
    return count

def analyze_sentiment(text_content):
    client = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = {"content": text_content, "type_": type_}
    
    response = client.analyze_sentiment(request = {'document': document})
    
    return response.document_sentiment.score

#Read json file
f = open('./news.json')
news = json.load(f)

assert isEnglish(news)

count = countSentence(news)
pbar = tqdm(total=count, ncols=80)
scores = []
start  = time.time()

for text in news:
    title_score  = analyze_sentiment(text["title"])
    subhead_score = analyze_sentiment(text["subhead"])
    para_score = []
    for para in text["article"]:
        para_score.append(analyze_sentiment(para))
        pbar.update(1)
    scores.append(0.2 * title_score + 0.1 * subhead_score + 0.7 * sum(para_score)/len(para_score))
print("Program Execution Time: "+str(time.time()-start)+" seconds. "+str(count)+" paragraphs has been analyzed")

#Visualization
x = range(10)
fig =  px.bar(x, y = scores)
fig.show()
