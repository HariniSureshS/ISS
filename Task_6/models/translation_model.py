import torch
import fairseq
de2en = torch.hub.load('pytorch/fairseq','transformer.wmt19.de-en',tokenizer='moses',bpe='fastBPE')
en2de = torch.hub.load('pytorch/fariseq','transformer.wmt19.en-de',tokenizer='moses',bpe='fastBPE')
de2en.eval()
en2de.eval()
assert isintance(en2de.models[0], fairseq.models.transformer.TransformerModel)
assert isintance(de2en.models[0], fairseq.models.transformer.TransformerModel)
language_dictionary = {'en2de': en2de, 'de2en':de2en}

def get_translation(query,from_lang,to_lang):
    input_lang_trans = from_lang + '2' + to_lang
    return language_dictionary[input_lang_trans].translate(query)
 
