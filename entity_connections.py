from itertools import islice
from cr import coreference_resolution
from preprocess import *

"""
https://dh2016.adho.org/abstracts/297
The first network is based on co-occurrences of characters in the same window of text: 
an edge between two characters exists if they are mentioned in the same paragraph and the weight of the edge is 
the number of paragraphs in which this is the case.
"""


def first_or_second(entity1, entity, count, connection_list):
    # found entity
    # first or second entity?
    if entity1 is None:
        # first
        entity1 = entity
    else:
        if count < 15 and entity1 != entity:
            # second
            a = False
            b = False
            for link in connection_list:
                for i, ent in enumerate(link):
                    if i != 2 and entity1[0] == ent[0]:
                        a = True
                    if i != 2 and entity[0] == ent[0]:
                        b = True
                if a and b:
                    link[2] += 1
                    break
            if not a or not b:
                connection_list.append([entity1, entity, 1])
        # first
        entity1 = entity
        count = 0

    return entity1, count, connection_list


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
    previous_entity = None
    i = 0
    while i < len(token_list):
        token = token_list[i]

        entity = []
        for ent in entity_list:
            for alias in ent:
                full_entity_name = str(alias).split(" ")  # "Hari Seldon" -> ["Hari", "Seldon"]
                if len(full_entity_name) == 1 and str(token) == str(alias):
                    # candidate has only name
                    entity.append(ent)
                    break
                elif len(full_entity_name) > 1 and str(token) == full_entity_name[0] and str(token_list[i + 1]) == \
                        full_entity_name[1]:
                    entity.append(ent)
                    break
                elif len(full_entity_name) > 1 and str(token) == full_entity_name[1]:
                    entity.append(ent)
                    break

        #ToDo: Coreference resolution
        # Example: token = 'Seldon', get correct candidate from entity_list
        # https://towardsdatascience.com/how-to-make-an-effective-coreference-resolution-model-55875d2b5f19
        # https://neurosys.com/article/most-popular-frameworks-for-coreference-resolution/
        if len(entity) > 0:
            entity = coreference_resolution(entity, token_list[i-10:i+10])
            previous_entity, count, connection_list = first_or_second(previous_entity, entity, count, connection_list)
        count += 1
        i += 1
        print(i, "out of ", len(token_list))

    return connection_list
