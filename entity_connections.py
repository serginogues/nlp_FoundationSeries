from itertools import islice
from preprocess import *

"""
https://dh2016.adho.org/abstracts/297
The first network is based on co-occurrences of characters in the same window of text: 
an edge between two characters exists if they are mentioned in the same paragraph and the weight of the edge is 
the number of paragraphs in which this is the case.
"""

def count_ngrams(iterable,n=2):
    return Counter(zip(*[islice(iterable, i, None) for i in range(n)]))

def entity_relationship(entity_list, text):
    """
    For each entity
        For each sentence in text
            if entity is in sentence
    :return: a list of tuples
    """
    # 0 - preprocessing
    text = re.sub(', ', ' ', str(text))  # removing new line characters
    text = re.sub(',', ' ', str(text))
    text = re.sub('- ', '', str(text))
    text = re.sub('-', ' ', str(text))
    text = re.sub('\n ', '', str(text))
    text = re.sub('\n', ' ', str(text))

    token_list = word_tokenize(text)
    token_list = [x for x in token_list if str(x) not in punctuation_tokens]
    connection_list = []
    count = 0
    entity1 = None
    for i, token in enumerate(token_list):
        entity = [x for x in entity_list if str(token) in x]
        if len(entity) > 0:
            # found entity
            # first or second entity?
            if entity1 is None:
                # first
                entity1 = entity[0]
            else:
                if count < 10 and entity1 != entity[0]:
                    # second
                    conn = [x for x in connection_list if entity1 in x and entity[0] in x]
                    if any(conn):
                        conn[0][2] += 1
                    else:
                        connection_list.append([entity1, entity[0], 1])

                    # print("found link between ", entity1, "and ", entity[0], "in sentence ", " ".join(token_list[i-20:i+20]))
                # first
                entity1 = entity[0]
                count = 0

        count += 1

    return connection_list
