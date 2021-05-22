"""
Rule-Based Named Entity Recognition model for the detection of character occurrences
"""
from config import tqdm, honorific_words, person_verbs, matcher, location_name_pattern, location_name, \
    travel_to_pattern, travel_to_verbs, nlp, punctuation_tokens
from utils import get_ents_from_doc, write_list, read_list, ner_unclassified_per, ner_unclassified_loc


def get_full_name(doc, token):
    full_name = [x for x in doc.ents if str(token) in str(x) and len(x) > 1]
    if len(full_name) > 0:
        return full_name[0]
    else:
        return token.text


def NER(sentence_list, STAGE=True, VALIDATE=False):
    """
    :param VALIDATE: if validate, there is no ovewritten in the txt files
    :return: labeled sentence list
    """
    print("Start NER")
    if STAGE:
        main_characters_ = []
        locations_ = []
        unclassified = []
        unclassified_sent = []
        predicted = []
        for sent in sentence_list:
            predicted.append(['O' for x in range(len(sent))])

        for i in tqdm(range(len(sentence_list))):
            doc = sentence_list[i]
            ents = get_ents_from_doc(doc)
            ents = [x for x in ents if len(x[0]) > 2 and not x[0].islower() and not x[0].isupper()]
            if any(ents):
                print(doc)
                for name, num_list in ents:
                    if len(num_list) > 1:
                        num = num_list[1]
                        token = doc[num]
                    else:
                        num = num_list[0]
                        token = doc[num]

                    if ner_person(doc, token, num):
                        main_characters_.append(name)
                        if len(num_list) == 1:
                            predicted[i][num_list[0]] = 'B-PER'
                        else:
                            predicted[i][num_list[0]] = 'B-PER'
                            predicted[i][num_list[1]] = 'I-PER'

                    elif ner_location(doc, token):
                        locations_.append(name)
                        if len(num_list) == 1:
                            predicted[i][num_list[0]] = 'B-LOC'
                        else:
                            predicted[i][num_list[0]] = 'B-LOC'
                            predicted[i][num_list[1]] = 'I-LOC'
                    else:
                        print("Unclassified: ", name, num_list)
                        unclassified.append([name, i])
                        unclassified_sent.append([name, i, num_list])

        location_list = list(set(locations_))
        people_list = list(set([x for x in main_characters_ if len(x) > 2]))
        for ent in people_list:
            if any([x for x in punctuation_tokens if x in ent]):
                people_list.remove(ent)

        # remove bad retrieved entities
        for ent, i in unclassified:
            if any([x for x in punctuation_tokens if x in ent]):
                unclassified.remove([ent, i])

        # NER unclassified
        for tup in unclassified:
            if tup[0] in people_list:
                ner_unclassified_per(predicted, unclassified_sent, tup)
            if tup[0] in location_list:
                ner_unclassified_loc(predicted, unclassified_sent, tup)

        if not VALIDATE:
            write_list('predicted', predicted)

    else:
        predicted = read_list('predicted')

    return predicted


def ner_person(doc, token, num):
    """
    :return: True if @token has person behaviour
    """
    if (token.dep_ == "nsubj" or token.dep_ == "dobj") and token.head.pos_ == 'VERB' and token.head.lemma_ in person_verbs:
        return True
    elif (num < len(doc)-1 and doc[num+1].text == "who") or (num < len(doc)-3 and doc[num+1].pos_ == "PUNCT" and doc[num+2].text == "who"):
        return True
    else:
        for i, word in enumerate(doc):
            if str(word) in honorific_words and i < len(doc) - 1 and doc[i + 1] == token:
                return True
    return False


def ner_location(doc, token):
    """
    1 - if sentence has PERSON, and within its coreferences in the sentence there is a location_noun e.g. 'planet'
    2 - if the sentence is of the form "VERB + to + PERSON" -> Person is a candidate of location
    :return: True if @token has location behaviour
    """
    matcher.add('location', [location_name_pattern])
    m = matcher(doc)
    for match_id, start, end in m:
        span = doc[start: end]
        for word in location_name:
            if word in str(span) and str(token) in str(span):
                return True

    matcher.add('location', [travel_to_pattern])
    m = matcher(doc)
    for match_id, start, end in m:
        span = doc[start: end]
        if len([x for x in nlp(str(span)) if x.pos_ == "VERB" and str(x.lemma_) in travel_to_verbs]) and str(
                token) in str(span):
            return True
