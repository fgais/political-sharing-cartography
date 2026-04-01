# political-sharing-cartography
Basic data processing steps to arrive at a Political Cartography of News Sharing. The data, which is should be stored in the folder `./data`, can be found on [Zenodo](https://zenodo.org/records/19071466). 

The basic steps of the research pipeline leading to a Political Cartography of News Sharing are described in 1.-4. These steps, in combination with the code, allow reproducing the lower-dimensional embedding using Correspondence Analysis (1.), the rotation of the corresponding embedding (2.), the collection of the articles (3.) and the topic modeling with STM in R (4.). 

The code to arrive at the figures/single plots in the paper "Introducing a Political Cartography of News Sharing: Capturing Story, Outlet and Content Level of News Circulation on Twitter" is listed under 5. and provided in the form of Jupyter Notebooks.

Code includes:
## 1. Correspondence Analysis
Run `01_Correspondence_Analysis.py` to carry out the Correspondence Analysis.  `01_Correspondence_Analysis.py` takes crosstab (`./data/followers_pseudo.csv`) file of following users (rows) and followed users (MPs) (columns) as input, 
```
|        | P_1 | P_2 | ... | P_N |
|--------+-----+-----+-----+-----|
| user_1 | int | ... | ... | int |
| ...... | int | ... | ... | int |
```
where an entry is 1 if the respective user follows the MP. The code simply needs to be executed with the crosstab saved in the `./data/` folder and then generates ideological embeddings of Twitter users with Correspondence Analysis, both for rows and columns, and exports these. 

## 2. Rotation and correlation with CHES data
Run `02_rotation.py` to correlate the embedding with CHES dimensions. `02_rotation.py` takes the 2019 CHES ([Chapel Hill Expert Survey](https://www.chesdata.eu/ches-europe)) file (needs to be downloaded and stored as `./data/CHES2019V3.csv`), as well as the party positions in the embedding that are supposed to be correlated with the CHES data. It take the positions of the MPs embedded via Correspondence Analysis, stored as `./data/mp_embedding_pseudo_before_rotation.csv`, and averages over their positions per party. It orthogonally combines the CHES left-right dimension with all other CHES dimensions and finds the rotation angle for each pair for which the combined Pearson Correlation of the two dimensions with two specified dimensions of the embedding is maximized. Then checks if the additional dimension (to the left-right dimension) can be constructed by averaging over the rotation angles of several high-correlation dimensions, with a cutoff of .8. Generates rotated embeddings according to the optimal rotation angle for parties and users and exports these rotated embeddings.

## 3. Article collection
Run `03_article_collection.py` to collect all articles that were shared during the observation period. `03_article_collection.py` takes a list of unique URLs from `shares_pseudo.csv` and subsequently collects article HTMLs, author, title and text, and stores them in a `.csv` file. (HTMLs are collected in case the `newspaper3k` library cannot process the text automatically.)

## 4. Topic model
Install the Python and R libraries from `requirements_tm_python.txt` and `requirements_tm_R.txt`, then run the following scripts:
- `04a_preprocessing.py`: lemmatize article texts and create documents for topic model
- `04b_stm.R`: infer STM for 20 to 300 topics (in steps of 20)
- `04c_compute_evals.R`: compute evaluation scores for the inferred models
- `04d_evaluate.ipynb`: plot evaluations, get topic labels and doc-topic-matrix

## 5. Plots of "Introducing a Political Cartography of News Sharing: Capturing Story, Outlet and Content Level of News Circulation on Twitter"
If the data from Zenodo has been downloaded and stored in the folder `./data/`, the plots of the paper can be reproduced with the following Jupyter notebooks which use `shares_pseudo.csv`, `embedding_pseudo.csv`, `article_topic_matrix.csv`, `article_to_id.csv` and `party_pos_FINAL.csv` ([Zenodo](https://zenodo.org/records/19071466)) which need to be stored in the `./data/` folder:
- The left panel of Fig. 1 and the right panel of Fig. 1, which are the two-dimensional embeddings before and after rotation, can be produced with `05a_plot_embedding.ipynb`.
- The plots for Fig. 2 A/B/C can be produced with `05b_plot_outlet_distribution_1D.ipynb`.
- The plots for Fig. 2 D/E/F and Fig. 3 C/E can be produced with `05c_plot_outlet_distribution.ipynb`.
- The plots for Fig. 3 A/B can be produced with `05d_plot_individual_articles.ipynb`.
- The plots for Fig. 3 D/F can be produced with `05e_plot_story_mean_distribution.ipynb`.
- The plots for Fig. 4 can be produced with `05f_plot_metatopic_x_outlet.ipynb`.
- The top plot in Fig. 5 can be produced with `05g_plot_metatopics.ipynb.ipynb`.
- The four plots below in Fig. 5 can be produced with `05h_plot_topics.ipynb`.


