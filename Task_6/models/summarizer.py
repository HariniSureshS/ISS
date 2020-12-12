from transformers import pipeline

LIMIT = 2500

summarizer = pipeline(task='summarization', model="bart-large-cnn")

# outputs list of text with at most LIMIT characters each
def split_text(text, limit, sep=" "):
    words = text.split()
    if max(map(len, words)) > limit:
        raise ValueError("limit is too small")
    res, part, others = [], words[0], words[1:]
    # 
    for word in others:
        if len(sep)+len(word) > limit-len(part):
            res.append(part)
            part = word
        else:
            part += sep+word
    if part:
        res.append(part)
    return res



def get_summarizer(query):
    '''
        gets summary of case text using BART abstractive summarizer trained
        on CNN/Daily. If the case text is less
        than the LIMIT number of characters, it simply gets the summary. If not, it cuts
        up the case text into strings that BART (1024 tokens) can handle then rejoins them
    '''

    if len(query) < LIMIT:
        summary = summarizer(query)
    else:
        list_of_summaries = split_text(query, LIMIT)
        summary = " ".join(list_of_summaries)


    return summary