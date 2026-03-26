import pandas as pd
import os
import csv
from newspaper import Article
from tqdm import tqdm
import sys

# Increase CSV field size to handle large HTML
csv.field_size_limit(sys.maxsize)

df = pd.read_csv('shares_pseudo.csv.zip')
unique_links = list(set(df.url))
print(f'There are {len(unique_links)} unique links in our edge list.')

# Check if some articles have already been downloaded
links_collected = set()
if os.path.isfile('articles.csv'):
    collected_df = pd.read_csv('articles.csv', chunksize=1000, engine='python')
    for chunk in collected_df:
        links_collected.update(chunk['link'].dropna())

# All links that have not been collected yet
res = [i for i in unique_links if i not in links_collected]

# Exception
res = [url.replace('http://visual.gnutiez.de:8082/hl_diff.html?jump=', '') 
       if 'http://visual.gnutiez.de' in url else url for url in res]

print(f'{len(res)} links have not been collected yet.')
print('Collection starts:')

with open('articles.csv', 'a', encoding='utf-8', newline='') as f:
    csvw = csv.writer(f, quoting=csv.QUOTE_ALL)

    for url in tqdm(res):
        try:
            article = Article(url)
            article.download()
            article.parse()

            # Write all collected info into one row
            csvw.writerow([
                url,
                article.title if hasattr(article, 'title') else None,
                article.text if hasattr(article, 'text') else None,
                article.authors if hasattr(article, 'authors') else None,
                article.html,
                'collected'  # status column
            ])

        except Exception as e:
            csvw.writerow([url, None, None, None, f'error: {e}', 'error'])
