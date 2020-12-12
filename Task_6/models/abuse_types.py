import re
import spacy
import en_core_web_lg

nlp = en_core_web_lg.load()
stop_words = list(nlp.Defaults.stop_words)

abuses = ['abandon' 'molest', 'beat', 'fight', 'divorce', 'threaten', 'drug', 'neglect']

def lemmatization(iss_str):
  tokens_list = []
  newString = ''
  for token in nlp(iss_str):
    tokens_list.append(token.lemma_)
  s = ' '.join(tokens_list)
  s = re.sub(r'-+[a-zA-Z]+-+', '', s)
  return s


def stop_word_removal(tokens):
  token_list = []
  for token in tokens:
    if token not in stop_words:
      token_list.append(token)
  s = ' '.join(token_list)
  newString = lemmatization(s)
  return newString


def cleaner(iss_str):
  specials = [r'[()]', r'[.,]', r'\n', r'st\b', r'–', r'…', r'[“”]', r'[\"]', r'’s', r'[;:?]', r'[-]']
  for special in specials:
    iss_str = re.sub(special, ' ', iss_str)
  iss_str = iss_str.lower()
  tokens = iss_str.split()
  newString = stop_word_removal(tokens)
  return newString


def pos_tagging_verb(string):
  pos_verbs = []
  string = nlp(string)
  for token in string:
    if(token.tag_ == 'VB' or token.tag_ == 'VBD' or token.tag_ == 'VBG' or token.tag_ == 'VBN' or token.tag_ == 'MD' or token.tag_ == 'VBP' or token.tag_ == 'VBZ'):
      pos_verbs.append(token.text)
  pos_verbs = list(set(pos_verbs))
  return pos_verbs


def get_abuse_scores(verb_list):
  abuse_scores = {'abandon':0, 'molest':0, 'beat':0, 'fight':0, 'divorce':0, 'threaten':0, 'drug':0, 'neglect':0}
  for word in verb_list:
    abuse_scores['abandon'] += nlp('abandon').similarity(nlp(word))
    abuse_scores['molest'] += nlp('molest').similarity(nlp(word))
    abuse_scores['beat'] += nlp('beat').similarity(nlp(word))
    abuse_scores['fight'] += nlp('fight').similarity(nlp(word))
    abuse_scores['divorce'] += nlp('divorce').similarity(nlp(word))
    abuse_scores['threaten'] += nlp('threaten').similarity(nlp(word))
    abuse_scores['drug'] += nlp('drug').similarity(nlp(word))
    abuse_scores['neglect'] += nlp('neglect').similarity(nlp(word))
  return abuse_scores


def abuse_types(case_text):
  clean_case = cleaner(case_text)
  pos_verbs = pos_tagging_verb(clean_case)
  abuse_type_to_score = get_abuse_scores(pos_verbs)

  types_only = abuse_type_to_score.keys()
  scores_only = abuse_type_to_score.values()
  abuse_score_to_type = dict(zip(scores_only, types_only))

  sorted_scores = sorted(scores_only)
  first_max = sorted_scores[-1]
  second_max = sorted_scores[-2]

  return [abuse_score_to_type[first_max].capitalize(), abuse_score_to_type[second_max].capitalize()]
