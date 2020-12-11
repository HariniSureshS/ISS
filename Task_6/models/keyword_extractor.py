from rake_nltk import Rake
import re
from collections import Counter
from nltk.corpus import stopwords

## add more English stopwords
stop_words = stopwords.words('english')
add_stopwords = ['due', 'following', 'via', 'mobile', 'whatsapp', 'since', 'however']
stop_words.extend(add_stopwords)

class KeywordExtractor:

  def __init__(self):
    self.rake_instance = Rake()

  def preprocess_text(self, text):

    ## remove special characters
    text = re.sub('\s+',' ', text)
    return text

  # def text_summarization(self, text):

  #   ## initialize BERT model
  #   model = Summarizer()
  #   result = model(body=text, num_sentences=self.num_sentences)

  #   ## prep final result
  #   summary = "".join(result)
  #   return summary

  def clean_extracted_keywords(self, word_list):

    ## remove stopwords
    updated_wordlist = []
    stopwords_dict = Counter(stop_words)
    for keyword in word_list:

      # output string
      temp_str = ''

      ## if there is "Case" word present, then dont remove numbers
      if 'case' not in keyword:
        keyword = re.sub('\d+', '', keyword)

      keyword = re.sub(r'[^\w\s]', '', keyword)

      ## for each word, remove stopwords (if any)
      for word in keyword.split():
        if word not in stopwords_dict:
          if len(word) > 2:
            temp_str += word + " "

      if temp_str:
        if len(temp_str.split()) > 2:
          updated_wordlist.append(temp_str)

    ## remove whitespaces
    updated_wordlist = [word.strip() for word in updated_wordlist]
    return updated_wordlist

  def keyword_extraction(self, text):

    ## extract keywords
    self.rake_instance.extract_keywords_from_text(text)

    ## get keyword phrases ranked highest to lowest.
    words = self.rake_instance.get_ranked_phrases( )
    clean_words = self.clean_extracted_keywords(words)

    return clean_words

  # def extract_entities(self, sentence):

  #   ## spacy pipeline
  #   doc = nlp(sentence)
  #   entities = {}

  #   ## extracting entities
  #   for ent in doc.ents:
  #     if ent.label_ not in entities.keys():
  #       entities[ent.label_] = []
  #       entities[ent.label_].append(ent.text)
  #     else:
  #       entities[ent.label_].append(ent.text)

  #   ## filter relevant entities
  #   required_entities = ['ORG', 'NORP', 'PERSON', 'GPE']
  #   updated_entities = {}
  #   for key, value in entities.items():
  #     if key in required_entities and len(value) > 0:
  #       updated_entities[key] = list(set(value))

  #   return updated_entities

  # def display_results(self, summary, keywords, relations):

  #   print('Case summary:')
  #   print()
  #   pprint.pprint(summary) # summary

  #   print('Relation tuples:')
  #   print()
  #   ## extract relation tuples
  #   for index in range(relations.shape[0]):
  #     relation = relations.iloc[index]['subject'] + ' --> ' + relations.iloc[index]['relation'] + ' --> ' + relations.iloc[index]['object']
  #     pprint.pprint(relation)
