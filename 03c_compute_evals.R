## Adapted from Julia Silge, "Training, evaluating, and interpreting topic models"
## https://juliasilge.com/blog/evaluating-stm/
## Licensed under  CC BY-SA 4.0

library(stm)
library(dplyr)
library(purrr)

print("Loading topics image...")
load("workspace_multitopics.RData")

print("Running evaluations...")

heldout <- make.heldout(docs,vocab)

k_result <- many_models %>%
  mutate(exclusivity = map(topic_model, exclusivity),
         semantic_coherence = map(topic_model, semanticCoherence, docs),
         eval_heldout = map(topic_model, eval.heldout, heldout$missing),
         residual = map(topic_model, checkResiduals, docs),
         bound =  map_dbl(topic_model, function(x) max(x$convergence$bound)),
         lfact = map_dbl(topic_model, function(x) lfactorial(x$settings$dim$K)),
         lbound = bound + lfact,
         iterations = map_dbl(topic_model, function(x) length(x$convergence$bound)))

print("Saving...")
save.image("workspace_multitopics_eval.RData")
