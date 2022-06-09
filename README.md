# Summer-2022-Programming-Challenge

### JSON file structure
    .
    ├── ...
    ├── page              # A web page on the news site
    │   ├── url           # URL for this page
    │   ├── title         # Title of the article
    │   ├── subhead       # Subheading
    │   └── article       # Article text
    │          ├── ...          
    │          ├── paragraph          # One of the paragraphs
    │          └── ...                
    └── ...
### Running A Test
To collect news articles: `python scripts/news_scraping.py` \
To do a basic sentiment analysis: `python scripts/sentiment.py`
#### Expected operation time
Approach 1: 49s (requires internet access) \
Approach 2: 6.5s

## Web Scraping
1. Make a request to the news site homepage with package 'requests'
2. Parse the resonse with BeautifulSoup
3. Find the links for the news article
4. Parse received articles and remove unrelevent texts with regex
5. Save to a json file
## Sentiment Analysis 
#### Approach 1: Sentiment Analysis from Google Cloud Natural Language API (online, faster)
#### Approach 2: Flair (offline, slower)
Run a sentiment analysis on each paragraph. Take the average of the scores. \
Also run sentiment analyses on title and subheading. \
Final Score = 0.3 * score of title + 0.3 * score of subheading + 0.4 * average of content
## Result
![Alt text](flair-result.png?raw=true "Title")
