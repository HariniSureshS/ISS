from transformers import pipeline

LIMIT = 2500

# outputs list of text with at most LIMIT characters each
def split_text(text, limit, sep=" "):
    words = text.split()
    if max(map(len, words)) > limit:
        raise ValueError("limit is too small")
    res, part, others = [], words[0], words[1:]

    for word in others:
        if len(sep)+len(word) > limit-len(part):
            res.append(part)
            part = word
        else:
            part += sep+word
    if part:
        res.append(part)
    return res


def get_summarizer(case_text):
    '''
        gets summary of case text using BART abstractive summarizer trained
        on CNN/Daily. If the case text is less
        than the LIMIT number of characters, it simply gets the summary. If not, it cuts
        up the case text into strings that BART (1024 tokens) can handle then rejoins them
    '''
    summarizer = pipeline(task='summarization', model="facebook/bart-large-cnn")

    summary = None
    if len(case_text) < LIMIT:
        summary = summarizer(case_text)
    else:
        list_of_summaries = split_text(case_text, LIMIT)
        summary = " ".join(list_of_summaries)

    return summary
