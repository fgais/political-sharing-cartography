## Adapted from Julia Silge, "Training, evaluating, and interpreting topic models"
## https://juliasilge.com/blog/evaluating-stm/
## Licensed under  CC BY-SA 4.0

library(dplyr)
library(stm)
library(furrr)
library(purrr)
library(tidyverse)

print("Loading data...")
data <- read.csv("<PATH_TO_PREPROCESSED_DATA>",
                 header = TRUE,
                 stringsAsFactors = FALSE,
                 # nrows = 100
                )

data$text <- gsub("\\|"," ",data$doc_lemmatized)

print("Preprocessing...")
processed <- textProcessor(data$text,
                           metadata = data,
                           removenumbers = FALSE,
                           removepunctuation = FALSE,
                           stem = FALSE, ## we already did that in spacy
                           removestopwords = FALSE ## we already did that in spacy
                           )

out <- prepDocuments(processed$documents,processed$vocab,processed$meta)
docs <- out$documents
vocab <- out$vocab
meta <- out$meta

print("Running model inference...")
plan(multisession, workers = 40)

many_models <- tibble(K = c(20,40,60,80,100,120,140,160,180,200,220,240,260,280,300)) %>%
    mutate(topic_model = future_map(
          K, ~ stm(documents = out$documents, vocab = out$vocab, K = ., data=out$meta, verbose = FALSE), 
          .options = furrr_options(seed = TRUE)
     ))

## save workspace image
save.image("workspace_multitopics.RData")
