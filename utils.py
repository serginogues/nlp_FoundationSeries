"""
Set of methods that could be useful at some point and some other deprecated
"""

from config import *


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


def first_or_second(entity1, entity, count, connection_list, span):
    """
    Deprecated
    """
    # found entity
    # first or second entity?
    if entity1 is None:
        # first
        entity1 = entity
    else:
        if count < 35:
            # second
            connection_list = check_exist(connection_list, entity1, entity)
        # first
        entity1 = entity
        count = 0

    return entity1, count, connection_list


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
