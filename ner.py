"""
Detection of Character Occurrences
"""

from utils import *

honorific_words = ['Dr.', 'Prof.', 'Mr.', 'Ms.', 'Msr.', 'Jr.', 'Sr.', 'Lord']
person_verbs_ = ['said', 'sniffed',  'met', 'greet', 'walked', 'respond', 'talk', 'think', 'hear', 'go', 'wait', 'pause', 'write', 'smile', 'answer', 'wonder', 'reply', 'read', 'sit', 'muttered', 'fumble', 'ask', 'sigh']
person_verbs = [lemmatization(w, 'v') for w in person_verbs_]
location_name = ['planet', 'kingdom', 'world', 'region', 'location', 'republic']
location_name_pattern = [{'POS': 'NOUN'}, {'LOWER': 'of'}, {'POS': 'PROPN'}]
travel_to_verbs_ = ['go', 'travel', 'move', 'exiled']
travel_to_verbs = [lemmatization(w, 'v') for w in travel_to_verbs_]
travel_to_pattern = [{'POS': 'VERB'}, {'LOWER': 'to'}, {'POS': 'PROPN'}]
be_in_pattern = [{'POS': 'AUX'}, {'LOWER': 'in'}, {'POS': 'PROPN'}]
be_on_pattern = [{'POS': 'AUX'}, {'LOWER': 'on'}, {'POS': 'PROPN'}]


def entity_identification(parsed_list):
    """
    :return: chronological sequence of unified character and location occurrences
    """
    # 3 - NER
    main_characters_ = []
    locations_ = []
    for i in tqdm(range(len(parsed_list))):
        doc = parsed_list[i]
        for token in doc:
            if token.pos_ == 'PROPN' and str(token) not in honorific_words:
                if detect_main_character(doc, token):
                    full_name = [x for x in doc.ents if str(token) in str(x) and len(x) > 1]
                    if len(full_name) > 0:
                        main_characters_.append(full_name[0])
                    else:
                        main_characters_.append(token.text)
                if detect_location(doc, token):
                    full_name = [x for x in doc.ents if str(token) in str(x) and len(x) > 1]
                    if len(full_name) > 0:
                        locations_.append(full_name[0])
                    else:
                        locations_.append(token.text)

    people_tuple_list = Counter(main_characters_).most_common(180)
    people_tuple_list = [x[0] for x in people_tuple_list if int(x[1]) > 1]
    location_tuple_list = Counter(locations_).most_common(150)
    location_tuple_list = [x[0] for x in location_tuple_list]

    return people_tuple_list, location_tuple_list


def detect_main_character(doc, token):
    """
    :return: True if @token has person behaviour
    """
    if token.dep_ == "nsubj" and token.head.pos_ == 'VERB' and token.head.lemma_ in person_verbs:
        return True
    else:
        for i, word in enumerate(doc):
            if str(word) in honorific_words and i < len(doc)-1 and doc[i+1] == token:
                return True
    return False


def detect_location(doc, token):
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
        if len([x for x in nlp(str(span)) if x.pos_ == "VERB" and str(x.lemma_) in travel_to_verbs]) and str(token) in str(span):
            return True
