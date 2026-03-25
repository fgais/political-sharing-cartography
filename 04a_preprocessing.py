import pandas as pd
import spacy
from tqdm import tqdm
import re
from langdetect import detect

DATA_PATH = <path_to_articles>
OUTPUT_PATH = <path_to_save_preprocessed_articles>

def fix_hyphens_in_tokenizer(nlp):
    from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
    from spacy.util import compile_infix_regex

    ## https://stackoverflow.com/a/58112065
    infixes = (
        LIST_ELLIPSES
        + LIST_ICONS
        + [
            r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
            ),
            r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
            #r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
            r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
        ]
    )
    infix_re = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_re.finditer
    return nlp

def lemmatize(doc,verbose=False):
    """
    This lemmatizer is smart, because it takes into account named entities!
    """
    tokenlist = []
    lemmatized_tokens = []
    named_entity_buffer = []

    for token in doc:    
        
        if token.ent_type_ in ['PER','LOC','GPE','ORG']:
            if verbose:
                print(token)
                print(token.ent_type_)
            named_entity_buffer.append(token)
        elif named_entity_buffer:
            tokenlist.append(named_entity_buffer)
            named_entity_buffer = []
            tokenlist.append(token)
        else:
            tokenlist.append(token)
    
    if named_entity_buffer:
        tokenlist.append(named_entity_buffer)
        
    ## re-iterate over the tokens to keep only the good ones
    for token in tokenlist:
        if type(token) == list:
            tokenset_string = []
            for t in token:
                tokenset_string.append(t.lemma_)
            final_ner_token = "_".join(tokenset_string)
            final_ner_token = final_ner_token.replace("\n","")
            final_ner_token = final_ner_token.replace("--","")
            ## make sure the first and last elements are not _
            if len(final_ner_token) > 0:
                if final_ner_token[0] == "_":            
                    final_ner_token = final_ner_token[1:]
            if len(final_ner_token) > 0:
                if final_ner_token[-1] == "_":
                    final_ner_token = final_ner_token[:-1]                    
            ## if there are two _ _ then it is usually two NERs together!            
            lemmatized_tokens.extend(final_ner_token.split("__"))
            
        else:
            if token.is_alpha and not token.is_stop:
                lemmatized_tokens.append(token.lemma_)
    return [i.lower() for i in lemmatized_tokens]

def remove_urls(text):
    text = re.sub(r'\(http\S+', '', text)
    text = re.sub(r'http\S+', '', text)
    return text

def clean_titles(string):
    if string == "unknown":
        return ""
    else:
        return string
    
def get_language(string):
    return detect(string)    

print("Loading spacy model...")
nlp = spacy.load("de_core_news_lg")
nlp = fix_hyphens_in_tokenizer(nlp)

print("Loading data...")
df = pd.read_csv(DATA_PATH)

print("Cleaning titles...")
df['title'] = df['title'].apply(clean_titles)
df['document'] = df['title'] + " " + df['text']

print("Removing URLs from articles...")
df['documents_clean'] = df['document'].apply(remove_urls)

print("Detecting language...")
df['langdetect'] = df['documents_clean'].apply(get_language)
df = df[df['langdetect'] == 'de']

documents = list(df['documents_clean'])
N_documents = len(documents)

print("Lemmatizing...")
documents_lemmatized = []
for d in tqdm(nlp.pipe(documents,n_process=15),total=N_documents):
    documents_lemmatized.append(lemmatize(d))

dlstrings = ["|".join(i) for i in documents_lemmatized]
df['doc_lemmatized'] = dlstrings

print("Saving...")
df[['article_id','title','outlet','link','doc_lemmatized','langdetect']].to_csv(OUTPUT_PATH,index=False)
