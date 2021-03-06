from config import sent_tokenize, re, tqdm, nlp


def preprocess(text, STAGE=True):
    """
    Remove unwanted characters + split by sentences + sentence tokenization + parsing + lemmatization + POS tagging
    """
    print("Start PREPROCESS")
    doc_list = []
    if STAGE:
        sentences = get_texts(text)
        print("Number of preprocessed sentences: ", len(sentences))
        for i in tqdm(range(len(sentences))):
            doc_list.append(nlp(sentences[i]))
    return doc_list


def get_sentences(text):
    text = remove_from_text(text)
    sentences = sent_tokenize(text)
    sentences = [re.sub(' +', ' ', sent) for sent in sentences]
    return sentences


def get_texts(text):
    a = text.split("\n\n")
    sentences = [remove_from_text(x) for x in a if x and not x.islower() and not x.isupper() and len(x) > 5]
    sentences = [re.sub(' +', ' ', sent) for sent in sentences]
    return sentences


def remove_from_text(text):
    """
    Remove new line characters and commas
    """
    # 0 - preprocessing
    """text = re.sub(', ', ' ', str(text))
    text = re.sub(',', '', str(text))"""
    text = re.sub('\n ', '', str(text))
    text = re.sub('\n', '', str(text))

    return text


def split_by_num_charcacters(text, n=500000):
    """
    https://stackoverflow.com/questions/9475241/split-string-every-nth-character
    """
    return [text[i:i + n] for i in range(0, len(text), n)]
