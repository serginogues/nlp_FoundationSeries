"""
Set of methods that could be useful at some point and some other deprecated
"""

from config import displacy, spacy, word_tokenize, punctuation_tokens, ngrams, PorterStemmer, lemmatizer, tee, \
    honorific_words, combinations


def dependency_graph(doc):
    """
    :param doc: doc = nlp(sentence)
    :return: saves render.html with the POS tagging and words relationship
    Dependency grammar example:
    TOM <-nsubj- CANCELED (root) --------dobj------------> FLIGHTS --nmod-> HOUSTON
                                    [THE MORNING]                    [TO]
    - CANCELED is the predicate (root)
    - TOM is the subject (nsubj)
    - FLIGHTS is the direct object (dobj)

    Clausal Argument relations:
        - NSUBJ - nominal subject
        - DOBJ - direct object
        - IOBJ - indirect object
        - CCOMP - clausal complement
        - XCOMP - open clausal complement

    Nominal Modifier relations:
        - NMOD - nominal modifier
        - AMOD - adjective modifier
        - NUMMOD - numeric modifier
        - APPOS - positional modifier
        - DET - Determiner
        - CASE prep, etz

    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_)
    """
    with open('renders/render.html', 'w') as f:
        f.write(displacy.render(docs=doc, page=True, options=dict(compact=True)))


def print_pos_tagging(doc):
    for token in doc:
        print(token.text, '=>', token.pos_, '=>', token.tag_, '=>', spacy.explain(token.pos_))


def tokenize_sentence(sentence, n=1):
    """
    :param sentence:
    :param n: n-gram tokenizer if n>1
    :return: token list
    """
    # tokenizer = RegexpTokenizer(r'\w+')  # TreebankWordTokenizer()
    tokens = sorted(word_tokenize(sentence))
    tokens = [x for x in tokens if x not in punctuation_tokens]  # remove punctuation if left

    if n > 1:
        n_gram = list(ngrams(tokens, n))
        tokens = [" ".join(x) for x in n_gram]

    return tokens


def get_lexicon(sentences):
    doc_tokens = []
    for sent in sentences:
        sent = sent.lower()
        tokens = tokenize_sentence(sent)
    all_doc_tokens = sum(doc_tokens, [])
    lexicon = sorted(set(all_doc_tokens))
    return lexicon


def update_progress(progress):
    print('\r[{0}] {1}%'.format('#' * (progress / 10), progress))


def stemming(word):
    """
    When should you use a lemmatizer or a stemmer? \n
    Both stemmers and lemmatizers will reduce your vocabulary size and increase the ambiguity of the text. But
    lemmatizers do a better job retaining as much of the information content as possible
    based on how the word was used within the text and its intended meaning.
    :returns: steemed word
    """
    stemmer = PorterStemmer()
    return stemmer.stem(word).strip("'")


def lemmatization(word, _pos="a"):
    """
    :param word:
    :param _pos: "a" == adjective, "n" == noun
    :return: lema of word
    """
    return lemmatizer.lemmatize(word, pos=_pos)


def coreference(parsed):
    """
    In: My sister has a dog. She loves him.\n
    Out: [My sister: [My sister, She], a dog: [a dog, him]]
    :param parsed: parsed = nlp(sentence)
    """
    cluster = parsed._.coref_clusters
    if len(cluster) > 0:
        cluster = cluster[0].mentions
    return cluster


def all_mentions(doc):
    """All the "mentions" in the given text:"""
    if doc._.has_coref:
        for cluster in doc._.coref_clusters:
            return cluster.mentions
    else:
        return None


def pronoun_references(doc):
    """Pronouns and their references:"""
    list = []
    for token in doc:
        # if token.pos_ == 'PRON' and token._.in_coref:
        for cluster in token._.coref_clusters:
            list.append((token.text, cluster.main.text))
    return list


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def is_candidate(token):
    return token.pos_ == 'PROPN' and str(token) not in honorific_words


def get_ents_from_doc(doc):
    """
    Return full named ents in doc
    :param doc:
    :return:
    """
    ents = []
    idx = 0
    for pair in pairwise(doc):
        if is_candidate(pair[0]) and is_candidate(pair[1]):
            ents.append([" ".join([pair[0].text, pair[1].text]), [idx, idx + 1]])
        elif is_candidate(pair[0]) and idx == 0:
            ents.append([pair[0].text, [idx]])
        elif is_candidate(pair[0]) and not idx == 0 and not is_candidate(doc[idx - 1]):
            ents.append([pair[0].text, [idx]])
        elif is_candidate(pair[1]) and not idx < len(doc) - 2:
            ents.append([pair[1].text, [idx + 1]])
        elif is_candidate(pair[1]) and idx < len(doc) - 2 and not is_candidate(doc[idx + 2]):
            ents.append([pair[1].text, [idx + 1]])
        idx += 1
    ents = remove_repe_from_list(ents)
    return ents


def remove_repe_from_list(list):
    """
    list[i] = [string, idx]
    """
    copy_list = list.copy()
    [list.remove(x[1]) for x in pairwise(copy_list) if x[0][0] == x[1][0]]
    return list


def solve_ambiguity_names(list, word):
    """
    There are some alias used for important characters in the text which can directly be solved without context
    """
    if word == 'Seldon':
        return ['Hari Seldon']
    elif word == 'Barr':
        # Ducem Bar is always explicitly written as 'Ducem Bar'
        return ['Onum Barr']
    elif word == 'Darell':
        # Darell alone is always referring to Dr.Darell
        return []
    elif word == 'Mallow':
        return []
    elif word == 'Foundation':
        return []
    else:
        return [list[0]]


def entity_from_token(entity_list, text):
    if len(text.split(" ")) > 1:
        return [x[0] for x in entity_list if x[0] == text]
    else:
        # text can be name or surname
        if not name_is_discardable(text):
            candidates = []
            [candidates.append(x[0][0]) for x in [(ent, ent[0].split(" ")) for ent in entity_list] if x[1][0] == text]
            [candidates.append(x[0][0]) for x in [(ent, ent[0].split(" ")) for ent in entity_list] if
             len(x[1]) > 1 and x[1][1] == text]
            if len(candidates) > 1:
                candidates = solve_ambiguity_names(candidates, text)

            if any(candidates):
                return candidates
            else:
                return []
        else:
            return []


def entity_from_word(entity_list, word):
    word = ""


def find_entities_in_doc(doc, entity_list):
    """
    :param text: sentence string
    :param entity_list: [['Hari Seldon'], ['Raven Seldon']]
    """
    list = [x for x in [entity_from_token(entity_list, word) for word in get_ents_from_doc(doc)] if x != []]
    return list


def name_is_discardable(text):
    """
    Some fictional characters have names which could be normal words like 'First Foundation' the word 'First'
    """
    discardable_names = ['Trader', 'Field', 'First', 'Grand', 'Master', 'Galactic', 'Second', 'Personal']
    list = text.split(" ")
    if any(list) and list[0] in discardable_names:
        return True
    else:
        return False


def is_name(alias, name, parsed=False):
    """
    len(alias) == 2 and len(
    Case 1:
        Name = Bayta
        alias = Bayta Darell
        return True because Name is the name of alias
    Case 2:
        Name = Darell
        alias = Bayta Darell
        return False because Name is the surname of alias
    """
    if parsed:
        for i, word in enumerate(alias):
            if i == 0 and str(word) == name:
                return True
        return False
    else:
        for i, word in enumerate(alias.split(" ")):
            if len(alias.split(" ")) > 1 and i == 0 and str(word) == name:
                return True
        return False


def write_list(name, list):
    with open('data_outputs/' + name + '.txt', 'w+') as f:
        f.seek(0)
        f.truncate()
        for item in list:
            if name == 'people_links' or name == 'location_links' or name == 'normalized' or name == 'predicted' or name == 'unclassified':
                a = ",".join([str(x) for x in item])
            else:
                a = item
            f.write('%s\n' % a)


def read_list(name):
    """
    Reads strings. Need to cast to type afterwards
    """
    list = []
    with open('data_outputs/' + name + '.txt', 'r') as f:
        for line in f:
            item = line[:-1]
            if name == 'people_links' or name == 'location_links' or name == 'normalized' or name == 'predicted':
                a = [x for x in item.split(',')]
                if name == 'people_links':
                    list.append([a[0], a[1], int(a[2])])
                elif name == 'location_links':
                    list.append([a[0], a[1], int(a[2])])
                elif name == 'unclassified':
                    list.append([a[0], int(a[1])])
                else:
                    list.append([x for x in a])
            else:
                list.append(item)
    return list
