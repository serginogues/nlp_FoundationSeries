from config import *

punctuation_tokens = {',', '.', '--', '-', '!', '?', ':', ';', '``', "''", '(', ')', '[', ']'}


def dependency_graph(doc):
    """
    :param doc: doc = nlp(sentence)
    :return: saves render.html with the POS tagging and words relationship
    """
    with open('render.html', 'w') as f:
        f.write(displacy.render(docs=doc, page=True, options=dict(compact=True)))


def subtree_matcher(doc):
    """
    https://www.analyticsvidhya.com/blog/2019/09/introduction-information-extraction-python-spacy/?utm_source=blog&utm_medium=nlp-project-information-extraction
    """
    subjpass = 0

    for i, tok in enumerate(doc):
        # find dependency tag that contains the text "subjpass"
        if tok.dep_.find("subjpass"):
            subjpass = 1

    x = ''
    y = ''

    # if subjpass == 1 then sentence is passive
    if subjpass == 1:
        for i, tok in enumerate(doc):
            if tok.dep_.find("subjpass"):
                y = tok.text

            if tok.dep_.endswith("obj"):
                x = tok.text

    # if subjpass == 0 then sentence is not passive
    else:
        for i, tok in enumerate(doc):
            if tok.dep_.endswith("subj"):
                x = tok.text

            if tok.dep_.endswith("obj"):
                y = tok.text

    return x, y


def print_pos_tagging(doc):
    for token in doc:
        print(token.text, '=>', token.pos_, '=>', token.tag_, '=>', spacy.explain(token.pos_))


def tokenize_sentence(sentence, n=1):
    """
    :param sentence:
    :param n: n-gram tokenizer if n>1
    :return: token list
    """
    tokenizer = RegexpTokenizer(r'\w+')  # TreebankWordTokenizer()
    tokens = sorted(tokenizer.tokenize(sentence))
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


"""def main_characters(sentences):
    word_list = []
    i = 0
    for sent in sentences:
        doc = nlp(sent)
        names = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
        word_list.append(names)
        i = i + 1
        print(i, " out of ", len(sentences))

    names = [line for line in word_list for line in set(line)]
    names_count = Counter(names).most_common(30)
    # print(pd.DataFrame(names_count))"""


def update_progress(progress):
    print('\r[{0}] {1}%'.format('#'*(progress/10), progress))


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
    lemmatizer = WordNetLemmatizer()
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


def check_results(people_tuple_list, location_tuple_list):
    n = 0
    for name in Target_people:
        if len([x for x in people_tuple_list if str(x[0]) in name]) > 0:
            n += 1
        else:
            print("Person -", name, "- not found")
    print(str((n/len(people_tuple_list))*100), "% of people found")

    n = 0
    for name in Target_locations:
        if len([x for x in location_tuple_list if str(x[0]) in name]) > 0:
            n += 1
        else:
            print("Location -", name, "- not found")
    print(str((n/len(Target_locations))*100), "% of locations found")
