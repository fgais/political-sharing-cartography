# political-sharing-cartography
Basic data processing steps to arrive at a Political Cartography of News Sharing. Includes:
## `01_Correspondence_Analysis.py`: Correspondence Analysis
Takes a crosstab `.csv` file of following users (rows) and followed users (such as parties or MPs) (columns) as an input, 
```
|        | P_1 | P_2 | ... | P_N |
|--------+-----+-----+-----+-----|
| user_1 | int | ... | ... | int |
| ...... | int | ... | ... | int |
```
where an entry is 1 if the respective user follows the MP. Generates ideological embeddings of Twitter users with Correspondence Analysis, both for rows and columns (output files need to be specified). 
## `02_rotation.py`: Rotation and correlation with CHES data
Takes the 2019 CHES ([Chapel Hill Expert Survey](https://www.chesdata.eu/ches-europe)) file (needs to be downloaded, `CHES2019V3.csv`), as well as the party positions in the embedding that are supposed to be correlated with the CHES data. 
Party positions should be a `.csv` file looking as follows:
```
| party  | dim_1 | ... | dim_N |
|--------+-------+-----+-------|
| party1 | float | ... | float |
| party2 | float | ... | float |
```
Paths to both files needs to be specified. Orthogonally combines the CHES left-right dimension with all other CHES dimensions and finds the rotation angle for each pair for which the combined Pearson Correlation of the two dimensions with two specified dimensions of the embedding is maximized. Then checks if the additional dimension (to the left-right dimension) can be constructed by averaging over the rotation angles of several high-correlation dimensions, with a cutoff of .8.

