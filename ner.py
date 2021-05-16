"""
Rule-Based Named Entity Recognition model for the detection of character occurrences
"""
from config import tqdm, Counter, honorific_words, person_verbs, matcher, location_name_pattern, location_name, \
    travel_to_pattern, travel_to_verbs, nlp, NER


def get_full_name(doc, token):
    full_name = [x for x in doc.ents if str(token) in str(x) and len(x) > 1]
    if len(full_name) > 0:
        return full_name[0]
    else:
        return token.text


def named_entity_recognition(sentence_list):
    """
    :return: chronological sequence of unified character and location occurrences
    """
    print("Start NER")
    if NER:
        main_characters_ = []
        locations_ = []
        for i in tqdm(range(len(sentence_list))):
            doc = sentence_list[i]
            for token in doc:
                if token.pos_ == 'PROPN' and str(token) not in honorific_words:
                    if ner_person(doc, token):
                        main_characters_.append(get_full_name(doc, token))

                    if ner_location(doc, token):
                        locations_.append(get_full_name(doc, token))

        people_list = Counter(main_characters_).most_common(180)
        people_list = [x[0] for x in people_list if int(x[1]) > 1]
        location_list = Counter(locations_).most_common(150)
        location_list = [x[0] for x in location_list]
    else:
        location_list = ['Trantor', 'Kalgan', 'Terminus', 'Anacreon', 'Synnax', 'Haven', 'Arcturus', 'Ahctuwus',
                         'Askone', 'Radole', 'Terminus City', 'Terminus City', 'Dellcass', 'Neotrantor', 'Gentri',
                         'Rossem', 'Space under Foundation']
        people_list = ['Darell', 'Seldon', 'Barr', 'Bayta', 'Mallow', 'Fie', 'Hardin', 'Toran', 'Gaal', 'Anthor',
                       'Stettin', 'Mis', 'Dorwin', 'Channis', 'Munn', 'Pritcher', 'Mule', 'Speaker', 'Arcadia',
                       'Brodrig', 'Pirenne', 'Sutt', 'Pappa', 'Randu', 'Magnifico', 'Indbur', 'Turbor', 'Verisof',
                       'Wienis', 'Ponyets', 'Jael', 'Forell', 'Sermak', 'Lepold', 'Gorov', 'Callia', 'Mayor', 'Fara',
                       'Master', 'Riose', 'Fran', 'Kleise', 'Mamma', 'Lee', 'Bort', 'Pherl', 'Chen', 'Walto', 'Aporat',
                       'Fox', 'Elders', 'Student', 'Semic', 'Avakim', 'Advocate', 'Lameth', 'Fulham', 'Empire', 'Orsy',
                       'Foundation', 'Capsule', 'Iwo', 'Mangin', 'Ovall', 'Hella', 'Commason', 'Plan', 'Meirus',
                       'Poochie', 'Palver']

    return people_list, location_list


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
