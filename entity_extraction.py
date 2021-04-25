from utils import *


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
    for doc in parsed_list:
        for token in doc:
            if detect_main_character(doc, token):
                full_name = [x for x in doc.ents if str(token) in str(x) and len(x) > 1]
                if len(full_name) > 0:
                    main_characters_.append(full_name[0])
                else:
                    main_characters_.append(token.text)

    people_list = Counter(main_characters_).most_common(150)
    """entity_people = []
    for name in people_list:
        list = [x for x in people_list if str(name) in str(x)]
        best = str(max(list, key=lambda t: len(str(t[0])))[0])
        tuple = (best, sum([int(x[1]) for x in list]))
        if best not in checked:
            entity_people.append(tuple)
            checked.append(best)"""

    people_list = [x for x in people_list if x[1] > 3]
    dict = pd.DataFrame(people_list, columns=['Name', 'Count'])

    return people_list, dict


def detect_main_character(doc, token):
    """
    token is a person (location or main character)
    1 - check person verbs
    """
    if token.pos_ == 'PROPN' and str(token) not in honorific_words:
        # if token behaves like a person
        if token.dep_ == "nsubj" and token.head.pos_ == 'VERB' and token.head.lemma_ in person_verbs:
            # print("Detected character, ", token, " with verb ", token.head.lemma_, "in sentence: \n", doc)
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
    print("Possible location: ", token, ", in following sentence: ", doc)
    is_location = False
    # 1
    coreference_list = coreference(doc)
    for mention in coreference_list:
        for location_word in location_nouns:
            if location_word in str(mention) and str(token) in str(mention):
                is_location = True

    # 2
    if not is_location:
        pattern = [{'POS': 'VERB'}, {'LOWER': 'to'}, {'POS': 'PROPN'}]
        matcher.add('location', [pattern])
        m = matcher(doc)
        for match_id, start, end in m:
            span = doc[start: end]
            if str(token) in str(span):
                is_location = True

    if is_location:
        print("location: ", token)
