# political-sharing-cartography
Basic data processing steps to arrive at a Political Cartography of News Sharing. Includes:
## 01_CA.py: Correspondence Analysis
Takes a crosstab `.csv` file of following users (rows) and followed users (such as parties or MPs) (columns), 
```
|        | P_1 | P_2| ... | P_N|
|--------+-----+----+-----+----|
| user_1 | int | ...| ... | int|
| ...... | int | ...| ... | int|
```
where an entry is 1 if the respective user follows the MP. Generates ideological embeddings of Twitter users with Correspondence Analysis, both for rows and columns. 
