# political-sharing-cartography
Basic data processing steps to arrive at a Political Cartography of News Sharing. Includes:
## 01_CA.py: Correspondence Analysis
Takes a crosstab `.csv` of users (rows) and MPs (columns), 
```
|  | MP_1    | MP_2 | ... | MP_N |
|------------+-------+----+-----+----|
| user_1        | float |    |     |    |
```
where an entry is 1 if the respective user follows the MP. Generates ideological embeddings of Twitter users with Correspondence Analysis, both for rows and columns. 
