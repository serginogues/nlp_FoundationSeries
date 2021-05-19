"""
Rule-Based Named Entity Recognition model for the detection of character occurrences
"""
from config import tqdm, Counter, honorific_words, person_verbs, matcher, location_name_pattern, location_name, \
    travel_to_pattern, travel_to_verbs, nlp, STAGE, punctuation_tokens
from utils import get_ents_from_doc


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
    if STAGE == 0:
        main_characters_ = []
        locations_ = []
        for i in tqdm(range(len(sentence_list))):
            doc = sentence_list[i]
            ents = get_ents_from_doc(doc)
            if any(ents):
                for name in ents:
                    list_ = [x for x in doc for y in name.split(" ") if str(x) == y]
                    if len(list_) > 1:
                        token = list_[1]
                    else:
                        token = list_[0]
                    if ner_person(doc, token):
                        main_characters_.append(name)

                    if ner_location(doc, token):
                        locations_.append(name)

        location_list = list(set(locations_))
        people_list = list(set([x for x in main_characters_ if len(x) > 2]))
        # people_list = Counter(people_list).most_common(2000)
        # people_list = [x[0] for x in people_list if int(x[1]) > 1]
        for ent in people_list:
            if any([x for x in punctuation_tokens if x in ent]):
                people_list.remove(ent)
        # TODO: normalization of entities with levenstein Soft-Idf
        # https://medium.com/enigma-engineering/improving-entity-resolution-with-soft-tf-idf-algorithm-42e323565e60

    else:
        location_list = ['Kalgan', 'Neotrantor', 'Synnax', 'Trantor', 'Rossem', 'Space', 'Terminus', 'Arcturus',
                         'Radole', 'Dellcass', 'Haven', 'Anacreon', 'Askone', 'Ahctuwus', 'Gentri']
        people_list = ['Star',
                       'Elders',
                       'Fran',
                       'Bayta',
                       'Transmitter',
                       'Whew',
                       'Crast',
                       'Dagobert IX',
                       'Senter',
                       'Han',
                       'Hella',
                       'Magnifico',
                       'Elvett',
                       'Asper',
                       'Barr',
                       'Erlking',
                       'Pelleas Anthor',
                       'Commissioners',
                       'Poochie',
                       'Empire',
                       'chauffeur',
                       'Cleon II',
                       'Bel',
                       'Bel Riose',
                       'Privy Secretary',
                       'Ovall',
                       'Channis',
                       'Asper Argo',
                       'Brodrig',
                       'Fulham',
                       'First Speaker',
                       'Lepold',
                       'Darell',
                       'Juddee',
                       'Gorm',
                       'Fox',
                       'Speaker',
                       'Haut Rodric',
                       'Radolian',
                       'Ducem Barr',
                       'Pritcher',
                       'Flan',
                       'Bail Channis',
                       'Grand Master',
                       'Emperor',
                       'Ponyets',
                       'Lewis',
                       'Argo',
                       'Twer',
                       'Haven',
                       'Second Foundation',
                       'Lieutenant Dirige',
                       'Hotel',
                       'Sammin',
                       'Dixyl',
                       'Lee Senter',
                       'Wienis',
                       'Linge Chen',
                       'Councilman',
                       'Master',
                       'Homir Munn',
                       'Palver',
                       'Indbur',
                       'Anthor',
                       'Amann',
                       'Hober Mallow',
                       'Mule',
                       'Meirus',
                       'Supervisor',
                       'Walto',
                       'Munn',
                       'Callia',
                       'Sutt',
                       'Pherl',
                       'Fleadquarters',
                       'Jole Turbor',
                       'Flober Mallow',
                       'Kalganese',
                       'Elvett Semic',
                       'Forell',
                       'Ebling Mis',
                       'Verisof',
                       'Kleise',
                       'Dirige',
                       'Galactography',
                       'Student',
                       'Randu',
                       'Tomaz Sutt',
                       'Yate Fulham',
                       'Arcadia',
                       'Capsule',
                       'Devers',
                       'Seldon',
                       'Pirenne',
                       'Sermak',
                       'Advocate',
                       'Aporat',
                       'Board',
                       'Lathan Devers',
                       'Hardin',
                       'Gaal',
                       'Bort',
                       'Turbor',
                       'Korell',
                       'Foundation',
                       'Jaim Twer',
                       'Space',
                       'Personal Capsule',
                       'Dornick',
                       'Rodric',
                       'Jael',
                       'Lundin Crast',
                       'Semic',
                       'Dad',
                       'Uncle Homir',
                       'Mamma',
                       'Homir',
                       'Tippellum',
                       'Commissioner',
                       'Askonian',
                       'Chairman',
                       'Salvor',
                       'Dorwin',
                       'Mallow',
                       'Sennett Forell',
                       'Twice Pritcher',
                       'Pappa',
                       'Mangin',
                       'Fara',
                       'Avakim',
                       'Les Gorm',
                       'Siwennian',
                       'Commason',
                       'Hari Seldon',
                       'Far Star',
                       'First',
                       'Jerril',
                       'Lameth',
                       'Mis',
                       'Salvor Hardin',
                       'Chen',
                       'Toran',
                       'Stettin',
                       'Luxor Hotel',
                       'Riose',
                       'Orsy',
                       'Gorov',
                       'Lee',
                       'Fie',
                       'Secretary',
                       'End',
                       'native',
                       'Iwo']

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
