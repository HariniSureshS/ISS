from models.keyword_extractor import stop_words
from models.abuse_types import nlp, abuses
import re

risk_factors = ['trauma', 'assault', 'abuse', 'harm', 'maltreat', 'sick', 'war', 'smuggle', 'kidnap', 'harass', 'poor', 'lack', 'turmoil', 'curse', 'deny', 'deport', 'crime', 'kill', 'arrest', 'prison']
risk_factors.extend(abuses)

# find words that have high similarity scores with any of the risk factors
# TODO: upon rendering, highlight those words
def get_risk_factors(case_text):
  lemma_to_orig = {}

  # remove special characters
  text = re.sub('\s+',' ', case_text)

  # lowercase text
  text = text.lower()

  # tokenize
  word_list = []
  for token in nlp(text):
    if token.text not in stop_words:
      lemmatized_word = token.lemma_
      word_list.append(lemmatized_word)

      # also save lemmatized word and its original in the lookup map
      lemma_to_orig[lemmatized_word] = token.text

  # get similarity scores between all words in the list and risk factors list, save words that have high similarity score with any of the risk factor
  high_similar_words_list = []
  for word in word_list:
    for risk_factor in risk_factors:
      similarity_score = nlp(risk_factor).similarity(nlp(word))
      if similarity_score >= 0.65:
        high_similar_words_list.append(word)
        break

  # return the original words from case text
  high_similar_original_words = []
  for word in high_similar_words_list:
    high_similar_original_words.append(lemma_to_orig[word])

  return list(set(high_similar_original_words))
