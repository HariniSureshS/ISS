from rake_nltk import Rake
import re
from collections import Counter
from nltk.corpus import stopwords

## add more English stopwords
stop_words = stopwords.words('english')
add_stopwords = ['due', 'following', 'via', 'mobile', 'whatsapp', 'since', 'however']
stop_words.extend(add_stopwords)

class KeywordExtractor:

  # def __init__(self, file_path, num_sentences):
    # self.file_path = file_path
    # self.num_sentences = num_sentences

  def __init__(self):
    self.rake_instance = Rake()

  # def extract_data_from_doc(self):

  #   # extract text
  #   text = docxpy.process(self.file_path)
  #   return text

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

  # def get_entity_pairs(self, text):
  #   # preprocess text
  #   text = re.sub(r'\n+', '.', text)  # replace multiple newlines with period
  #   text = re.sub(r'\[\d+\]', ' ', text)  # remove reference numbers
  #   text = nlp(text)

  #   def refine_ent(ent, sent):
  #       unwanted_tokens = (
  #           'PRON',  # pronouns
  #           'PART',  # particle
  #           'DET',  # determiner
  #           'SCONJ',  # subordinating conjunction
  #           'PUNCT',  # punctuation
  #           'SYM',  # symbol
  #           'X',  # other
  #       )
  #       ent_type = ent.ent_type_  # get entity type
  #       if ent_type == '':
  #           ent_type = 'NOUN_CHUNK'
  #           ent = ' '.join(str(t.text) for t in
  #                          nlp(str(ent)) if t.pos_
  #                          not in unwanted_tokens and t.is_stop == False)
  #       elif ent_type in ('NOMINAL', 'CARDINAL', 'ORDINAL') and str(ent).find(' ') == -1:
  #           refined = ''
  #           for i in range(len(sent) - ent.i):
  #               if ent.nbor(i).pos_ not in ('VERB', 'PUNCT'):
  #                   refined += ' ' + str(ent.nbor(i))
  #               else:
  #                   ent = refined.strip()
  #                   break

  #       return ent, ent_type

  #   sentences = [sent.string.strip() for sent in text.sents]  # split text into sentences
  #   ent_pairs = []
  #   for sent in sentences:
  #       sent = nlp(sent)
  #       spans = list(sent.ents) + list(sent.noun_chunks)  # collect nodes
  #       spans = spacy.util.filter_spans(spans)
  #       with sent.retokenize() as retokenizer:
  #           [retokenizer.merge(span, attrs={'tag': span.root.tag,
  #                                           'dep': span.root.dep}) for span in spans]
  #       deps = [token.dep_ for token in sent]
  #       for token in sent:
  #           if token.dep_ not in ('obj', 'dobj'):  # identify object nodes
  #               continue
  #           subject = [w for w in token.head.lefts if w.dep_
  #                      in ('subj', 'nsubj')]  # identify subject nodes
  #           if subject:
  #               subject = subject[0]
  #               # identify relationship by root dependency
  #               relation = [w for w in token.ancestors if w.dep_ == 'ROOT']
  #               if relation:
  #                   relation = relation[0]
  #                   # add adposition or particle to relationship
  #                   if relation.nbor(1).pos_ in ('ADP', 'PART'):
  #                       relation = ' '.join((str(relation), str(relation.nbor(1))))
  #               else:
  #                   relation = 'unknown'

  #               subject, subject_type = refine_ent(subject, sent)
  #               token, object_type = refine_ent(token, sent)

  #               ent_pairs.append([str(subject), str(relation), str(token),
  #                                 str(subject_type), str(object_type)])

  #   ent_pairs = [sublist for sublist in ent_pairs
  #                         if not any(str(ent) == '' for ent in sublist)]
  #   pairs = pd.DataFrame(ent_pairs, columns=['subject', 'relation', 'object',
  #                                            'subject_type', 'object_type'])
  #   print('Entity pairs extracted:', str(len(ent_pairs)))

  #   return pairs

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

  #   print()
  #   print('Important keywords:')
  #   print()
  #   keywords = [[word] for word in keywords]
  #   print(tabulate(keywords)) # keywords
  #   print()

  #   print('Relation tuples:')
  #   print()
  #   ## extract relation tuples
  #   for index in range(relations.shape[0]):
  #     relation = relations.iloc[index]['subject'] + ' --> ' + relations.iloc[index]['relation'] + ' --> ' + relations.iloc[index]['object']
  #     pprint.pprint(relation)
