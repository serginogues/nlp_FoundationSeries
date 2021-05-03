from utils import *


def preprocess(text):
    """
    Remove unwanted characters + split by sentences + sentence tokenization + lemmatization + POS tagging
    """
    # 0 - preprocessing
    text = re.sub(', ', ' ', str(text))  # removing new line characters
    text = re.sub(',', ' ', str(text))
    text = re.sub('\n ', '', str(text))
    text = re.sub('\n', ' ', str(text))

    # 1 - original sentence
    sentences = sent_tokenize(text)
    print("Number of sentences: ", len(sentences))
    sentences = [re.sub(' +', ' ', sent) for sent in sentences]

    # English tokenizer, tagger, parser and NER
    parsed_list = []
    for i in tqdm(range(len(sentences))):
        parsed_list.append(nlp(sentences[i]))
    print("Number of preprocessed sentences: ", len(parsed_list))

    return parsed_list





