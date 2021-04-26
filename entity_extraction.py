from utils import *
from coreference import *

honorific_words = ['Dr.', 'Prof.', 'Mr.', 'Ms.', 'Msr.', 'Jr.', 'Sr.', 'Lord']
person_verbs_ = ['said', 'sniffed',  'met', 'greet', 'walked', 'respond', 'talk', 'think', 'hear', 'go', 'wait', 'pause', 'write', 'smile', 'answer', 'wonder', 'reply', 'read', 'sit', 'muttered', 'fumble', 'ask', 'sigh']
person_verbs = [lemmatization(w, 'v') for w in person_verbs_]
location_name = ['planet', 'kingdom', 'world', 'region', 'location']
location_name_pattern = [{'POS': 'NOUN'}, {'LOWER': 'of'}, {'POS': 'PROPN'}]
travel_to_verbs_ = ['go', 'travel', 'move', 'exiled']
travel_to_verbs = [lemmatization(w, 'v') for w in travel_to_verbs_]
travel_to_pattern = [{'POS': 'VERB'}, {'LOWER': 'to'}, {'POS': 'PROPN'}]
be_in_pattern = [{'POS': 'AUX'}, {'LOWER': 'in'}, {'POS': 'PROPN'}]
be_on_pattern = [{'POS': 'AUX'}, {'LOWER': 'on'}, {'POS': 'PROPN'}]


def preprocess(text):
    # 0 - preprocessing
    text = re.sub('\n ', '', str(text))  # removing new line characters
    text = re.sub('\n', ' ', str(text))

    # 1 - original sentence
    sentences = sent_tokenize(text)
    print("Number of sentences: ", len(sentences))
    sentences = [re.sub(' +', ' ', sent) for sent in sentences]

    # 2 - Part of speech Tagging + 3 - shallow parsing
    parsed_list = []
    for i in tqdm(range(len(sentences))):  # len(sentences)
        parsed_list.append(nlp(sentences[i]))
    print("Number of parsed sentences: ", len(parsed_list))

    return parsed_list


def entity_identification(parsed_list):
    # 3 - NER
    main_characters_ = []
    locations_ = []
    for i in tqdm(range(len(parsed_list))):
        doc = parsed_list[i]
        for token in doc:
            if token.pos_ == 'PROPN':
                if detect_main_character(doc, token):
                    full_name = [x for x in doc.ents if str(token) in str(x) and len(x) > 1]
                    if len(full_name) > 0:
                        main_characters_.append(full_name[0])
                    else:
                        main_characters_.append(token.text)
                if detect_location(doc, token):
                    print(token)
                    full_name = [x for x in doc.ents if str(token) in str(x) and len(x) > 1]
                    if len(full_name) > 0:
                        locations_.append(full_name[0])
                    else:
                        locations_.append(token.text)

    locations_ = [x for x in locations_ if str(x) not in main_characters_]
    people_list = Counter(main_characters_).most_common(180)
    location_list = Counter(main_characters_).most_common(150)
    # people_list = [x for x in people_list if x[1] > 2]
    dict = pd.DataFrame(people_list, columns=['Name', 'Count'])

    return people_list, dict


def detect_main_character(doc, token):
    """
    :return: True if @token is person
    """
    if str(token) not in honorific_words:
        if token.dep_ == "nsubj" and token.head.pos_ == 'VERB' and token.head.lemma_ in person_verbs:
            return True
        else:
            for i, word in enumerate(doc):
                if str(word) in honorific_words and i < len(doc)-1 and doc[i+1] == token:
                    return True
    else:
        return False


def detect_location(doc, token):
    """
    1 - if sentence has PERSON, and within its coreferences in the sentence there is a location_noun e.g. 'planet'
    2 - if the sentence is of the form "VERB + to + PERSON" -> Person is a candidate of location
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
        if len([x for x in nlp(str(span)) if x.pos_ == "VERB" and str(x) in travel_to_verbs]) and str(token) in str(span):
            return True

    matcher.add('location', [be_in_pattern])
    m = matcher(doc)
    for match_id, start, end in m:
        span = doc[start: end]
        if len([x for x in nlp(str(span)) if (x.pos_ == "VERB" or x.pos_ == "AUX") and x.lemma_ == 'be']) and str(token) in str(span):
            return True

    matcher.add('location', [be_on_pattern])
    m = matcher(doc)
    for match_id, start, end in m:
        span = doc[start: end]
        if len([x for x in nlp(str(span)) if x.pos_ == "VERB" or "AUX" and x.lemma_ == 'be']) and str(token) in str(span):
            return True
