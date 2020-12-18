from summarizer import TransformerSummarizer

summarizer = TransformerSummarizer(transformer_type="XLNet",transformer_model_key="xlnet-base-cased")

def get_summary(case_text):
    '''
    get_summary:
        gets summary of case text using XLNET extractive summarizer.
        
    Input:
        case_text (str)    
    '''
    return ''.join(summarizer(case_text, min_length=60))
