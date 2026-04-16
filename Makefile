RAW_DATA_FILES = data/articles_to_id.csv data/article_topic_matrix.csv data/assigned_metatopics.csv data/embedding_pseudo_before_rotation.csv data/embedding_pseudo.csv data/followers_pseudo.csv data/mp_embedding_pseudo_before_rotation.csv data/party_pos_FINAL.csv data/shares_pseudo.csv data/CHES2019V3.csv

.PHONY: check_download 01 02 03 04 05

all: 05

$(RAW_DATA_FILES):
	uv run zenodo_get 19071466 -g "*.csv" -o ./data
	wget -O ./data/CHES2019V3.csv https://www.chesdata.eu/s/CHES2019V3.csv

check_download: $(RAW_DATA_FILES)
	echo "bd688b5247578489140393473e3f344a  ./data/articles_to_id.csv\n3e6892c873c0bce41cf508ddcaf780d1  ./data/article_topic_matrix.csv\n272701d4673c199f853f6e277c917625  ./data/assigned_metatopics.csv\n55e4edc8edc84ea7e05ce8c31c8c10be  ./data/embedding_pseudo_before_rotation.csv\n82676bc2a31e48afa59805faa6b5b62d  ./data/embedding_pseudo.csv\na26918e8fdd50cd9a64b0fb184b90a6e  ./data/followers_pseudo.csv\n98d007a0b503b170451e566b91162981  ./data/mp_embedding_pseudo_before_rotation.csv\nd33a9d48903cb685c277fbcdacba74b4  ./data/party_pos_FINAL.csv\nb088c4fbcaa28aa8dcb11925c0355d2a  ./data/shares_pseudo.csv" | md5sum -c
	echo "a31d2118b65216d13a7294f28381292b  data/CHES2019V3.csv" | md5sum -c

01: check_download
	uv run 01_Correspondence_Analysis.py

02: check_download
	uv run 02_rotation.py

03: check_download
	@echo SCRAPING ARTICLES, uncomment if you really want to do that
	# uv run 03_article_collection.py

04: check_download
	@Not possible without first running 03; also editing 04*.R

05: check_download
	# Take quite some time (expect 30+mins)
	uv run --with jupyter jupyter nbconvert --to html --execute 05*.ipynb
