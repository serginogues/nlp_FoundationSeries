"""
Rule-Based Named Entity Recognition model for the detection of character occurrences
"""
from config import tqdm, honorific_words, person_verbs, matcher, location_name_pattern, location_name, \
    travel_to_pattern, travel_to_verbs, nlp, punctuation_tokens
from utils import get_ents_from_doc, write_list, read_list


def get_full_name(doc, token):
    full_name = [x for x in doc.ents if str(token) in str(x) and len(x) > 1]
    if len(full_name) > 0:
        return full_name[0]
    else:
        return token.text


def named_entity_recognition(sentence_list, STAGE=True):
    """
    :return: chronological sequence of unified character and location occurrences
    """
    print("Start NER")
    if STAGE:
        main_characters_ = []
        locations_ = []
        unclassified = []
        PREDICTED = []
        for sent in sentence_list:
            PREDICTED.append(['O' for x in range(len(sent))])

        for i in tqdm(range(len(sentence_list))):
            doc = sentence_list[i]
            ents = get_ents_from_doc(doc)
            ents = [x for x in ents if len(x[0]) > 2 and not x[0].islower() and not x[0].isupper()]
            if any(ents):
                for name, num in ents:
                    list_ = [x for x in doc for y in name.split(" ") if str(x) == y]
                    if len(list_) > 1:
                        token = list_[1]
                    else:
                        token = list_[0]
                    if ner_person(doc, token):
                        main_characters_.append(name)
                        if len(num) == 1:
                            PREDICTED[i][num[0]] = 'B-PER'
                        else:
                            PREDICTED[i][num[0]] = 'B-PER'
                            PREDICTED[i][num[1]] = 'I-PER'

                    elif ner_location(doc, token):
                        locations_.append(name)
                        if len(num) == 1:
                            PREDICTED[i][num[0]] = 'B-LOC'
                        else:
                            PREDICTED[i][num[0]] = 'B-LOC'
                            PREDICTED[i][num[1]] = 'I-LOC'
                    else:
                        unclassified.append(name)

        location_list = list(set(locations_))
        people_list = list(set([x for x in main_characters_ if len(x) > 2]))
        for ent in people_list:
            if any([x for x in punctuation_tokens if x in ent]):
                people_list.remove(ent)
        unclassified = list(set(unclassified))
        unclassified = [x for x in unclassified if (x not in people_list and x not in location_list)]
        for ent in unclassified:
            if any([x for x in punctuation_tokens if x in ent]):
                unclassified.remove(ent)

        write_list('people_list', people_list)
        write_list('location_list', location_list)
        write_list('unclassified', unclassified)

    else:

        location_list = read_list('location_list')
        people_list = read_list('people_list')
        unclassified = read_list('unclassified')

    return people_list, location_list, unclassified


def ner_person(doc, token):
    """
    :return: True if @token has person behaviour
    """
    if token.dep_ == "nsubj" and token.head.pos_ == 'VERB' and token.head.lemma_ in person_verbs:
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


def ner_event(doc):
    """
    Fact analyses
    Most events are build around patterns of the form: <OBJECT> <VERB> <SUBJECT>
    #TODO: see course 5 slide 35
    """
    subject = ""
    direct_object = ""
    indirect_object = ""
    verb = ""
    # get token dependencies
    for word in doc:
        # subject would be
        if word.dep_ == "nsubj":
            subject = word.orth_
        # iobj for indirect object
        elif word.dep_ == "iobj":
            indirect_object = word.orth_
        # dobj for direct object
        elif word.dep_ == "dobj":
            direct_object = word.orth_
        elif word.dep_ == 'ROOT':
            verb = word
    if str(subject) != "" and str(verb) != "" and str(direct_object) != "":
        print("----------Event---------\n - '", doc.text, "'\n - Who? ", subject, "\n - What?: ", verb, "\n - vs Who? ",
              direct_object, "\n - indirect object: ", indirect_object)
