"""
Set of methods that could be useful at some point
"""

from config import *

punctuation_tokens = {',', '.', '--', '-', '!', '?', ':', ';', '``', "''", '(', ')', '[', ']', '...'}


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


# people_list = ['Darell',  'Seldon',  'Barr',  'Bayta',  'Mallow',  'Fie',  'Gaal',  'Hardin',  'Toran',  'Anthor',  'Stettin',  'Mis',  'Dorwin',  'Munn',  'Channis',  'Pritcher',  'Arcadia',  'Brodrig',  'Mule',  'Speaker',  'Pirenne',  'Pappa',  'Sutt',  'Randu',  'Indbur',  'Turbor',  'Magnifico',  'Verisof',  'Wienis',  'Commdor',  'Jael',  'Sermak',  'Lepold',  'Forell',  'Mayor',  'dryly',  'Kleise',  'Mamma',  'Chen',  'Fara',  'Lee',  'Bort',  'Master',  'Pherl',  'Fran',  'Semic',  'Walto',  'Aporat',  'Sir',  'Gorov',  'Fox',  'Elders',  'Palver',  'Avakim',  'Advocate',  'Lameth',  'Fulham',  'Empire',  'Gorm',  'Ponyets',  'Emperor',  'Riose',  'Foundation',  'Devers',  'Dad',  'Capsule',  'Iwo',  'Ovall',  'Hella',  'Commason',  'Plan',  'Student',  'Meirus',  'Poochie']
# location_list = ['Trantor',  'Kalgan',  'Anacreon',  'Terminus',  'Synnax',  'Haven',  'Arcturus',  'Ahctuwus',  'Askone',  'Radole',  'Dellcass',  'Neotrantor',  'Gentri',  'Rossem',  'Space under Foundation']
# final_list = [['Arkady Darell'], ['Hari Seldon'], ['Raven Seldon'], ['Fiari Seldon'], ['Seldon Hardin'], ['Ducem Barr'], ['Onum Barr'], ['Bayta Darell'], ['Hober Mallow'], ['Fie'], ['Gaal Dornick'], ['Salvor Hardin'], ['Toran Darell'], ['Pelleas Anthor'], ['Stettin'], ['Ebling Mis'], ['Dorwin'], ['Homir Munn'], ['Flomir Munn'], ['Bail Channis'], ['Han Pritcher'], ['Flan Pritcher'], ['Arcadia Darell'], ['Brodrig'], ['The Mule'], ['Speaker'], ['Lewis Pirenne'], ['Pappa'], ['Jorane Sutt'], ['Randu'], ['Indbur'], ['Jole Turbor'], ['Magnifico Giganticus'], ['Verisof'], ['Wienis'], ['Commdor Asper'], ['Ankor Jael'], ['Sef Sermak'], ['Lepold'], ['Sennett Forell'], ['Mayor Hardin'], ['dryly'], ['Kleise'], ['Mamma'], ['Linge Chen'], ['Jord Fara'], ['Yohan Lee'], ['Lee Senter'], ['Lewis Bort'], ['Master'], ['Pherl'], ['Fran'], ['Elvett Semic'], ['Walto'], ['Theo Aporat'], ['Eskel Gorov'], ['Fox'], ['Elders'], ['Preem Palver'], ['Avakim'], ['Advocate'], ['Lameth'], ['Fulham'], ['Galactic Empire'], ['Second Empire'], ['Les Gorm'], ['Limmar Ponyets'], ['Emperor'], ['Bel Riose'], ['Second Foundation'], ['Second Foundationer'], ['First Foundation'], ['Lathan Devers'], ['Dad'], ['Capsule'], ['Iwo'], ['Ovall Gri'], ['Hella'], ['Jord Commason'], ['Plan'], ['Student'], ['Lev Meirus'], ['Poochie']]

"""[[['Gaal Dornick'], ['Hari Seldon'], 2],
 [['Galactic Empire'], ['Emperor'], 44],
 [['Hari Seldon'], ['Raven Seldon'], 6],
 [['Fiari Seldon'], ['Hari Seldon'], 3],
 [['Avakim'], ['Hari Seldon'], 4],
 [['Advocate'], ['Hari Seldon'], 5],
 [['Second Empire'], ['Galactic Empire'], 27],
 [['Hari Seldon'], ['Linge Chen'], 4],
 [['Hari Seldon'], ['Fie'], 10],
 [['Salvor Hardin'], ['Seldon Hardin'], 55],
 [['Seldon Hardin'], ['Lewis Pirenne'], 33],
 [['Lewis Pirenne'], ['Second Foundation'], 118],
 [['Jorane Sutt'], ['Jord Fara'], 19],
 [['Jord Fara'], ['Fulham'], 3],
 [['Dorwin'], ['Galactic Empire'], 10],
 [['Mayor Hardin'], ['Seldon Hardin'], 8],
 [['Seldon Hardin'], ['dryly'], 2],
 [['Seldon Hardin'], ['Lameth'], 1],
 [['Fie'], ['Yohan Lee'], 16],
 [['Yohan Lee'], ['Sef Sermak'], 18],
 [['Verisof'], ['Mayor Hardin'], 11],
 [['Wienis'], ['Lepold'], 51],
 [['Hari Seldon'], ['Plan'], 64],
 [['Sef Sermak'], ['Lewis Bort'], 9],
 [['Sef Sermak'], ['Walto'], 6],
 [['Wienis'], ['Theo Aporat'], 2],
 [['Les Gorm'], ['Second Foundation'], 3],
 [['Capsule'], ['Limmar Ponyets'], 8],
 [['Les Gorm'], ['Eskel Gorov'], 18],
 [['Limmar Ponyets'], ['Master'], 22],
 [['Pherl'], ['Master'], 11],
 [['Pherl'], ['Elders'], 2],
 [['Jorane Sutt'], ['Hober Mallow'], 62],
 [['Second Foundation'], ['Commdor Asper'], 3],
 [['Onum Barr'], ['Ducem Barr'], 46],
 [['Hober Mallow'], ['Ankor Jael'], 25],
 [['Galactic Empire'], ['Bel Riose'], 66],
 [['Sennett Forell'], ['Hober Mallow'], 14],
 [['Brodrig'], ['Emperor'], 30],
 [['Bel Riose'], ['Lathan Devers'], 64],
 [['Dad'], ['Fran'], 11],
 [['Fran'], ['Randu'], 20],
 [['Fran'], ['Second Foundationer'], 3],
 [['The Mule'], ['Randu'], 135],
 [['Indbur'], ['Second Foundation'], 20],
 [['Flan Pritcher'], ['Han Pritcher'], 69],
 [['Second Foundation'], ['Magnifico Giganticus'], 2],
 [['Ebling Mis'], ['Indbur'], 63],
 [['Fran'], ['Iwo'], 2],
 [['Second Foundation'], ['Ovall Gri'], 5],
 [['Fox'], ['Han Pritcher'], 5],
 [['The Mule'], ['Jord Commason'], 9],
 [['Yohan Lee'], ['Lee Senter'], 6],
 [['First Foundation'], ['Second Foundation'], 50],
 [['The Mule'], ['Bail Channis'], 91],
 [['Speaker'], ['Fie'], 30],
 [['Arkady Darell'], ['Bayta Darell'], 23],
 [['Arcadia Darell'], ['Arkady Darell'], 4],
 [['Pelleas Anthor'], ['Arkady Darell'], 71],
 [['Toran Darell'], ['Arkady Darell'], 2],
 [['Student'], ['Speaker'], 18],
 [['Jole Turbor'], ['Elvett Semic'], 46],
 [['Homir Munn'], ['Arkady Darell'], 56],
 [['Pelleas Anthor'], ['Kleise'], 24],
 [['Flomir Munn'], ['Homir Munn'], 8],
 [['Stettin'], ['The Mule'], 15],
 [['Stettin'], ['Lev Meirus'], 6],
 [['Lev Meirus'], ['Poochie'], 7],
 [['Mamma'], ['Pappa'], 18],
 [['Pappa'], ['Preem Palver'], 12]]"""
"""links_list = [[['Gaal', 'Gaal Dornick'], ['Seldon', 'Hari Seldon'], 24],
 [['Empire', 'Galactic Empire'], ['Emperor'], 8],
 [['Empire', 'Galactic Empire'], ['Gaal', 'Gaal Dornick'], 1],
 [['Avakim'], ['Seldon', 'Hari Seldon'], 1],
 [['Emperor'], ['Avakim'], 2],
 [['Avakim'], ['Gaal', 'Gaal Dornick'], 3],
 [['Chen', 'Linge Chen'], ['Gaal', 'Gaal Dornick'], 3],
 [['Advocate'], ['Seldon', 'Hari Seldon'], 2],
 [['Empire', 'Galactic Empire'], ['Advocate'], 1],
 [['Seldon', 'Hari Seldon'], ['Empire', 'Galactic Empire'], 17],
 [['Chen', 'Linge Chen'], ['Seldon', 'Hari Seldon'], 2],
 [['Seldon', 'Hari Seldon'], ['Emperor'], 4],
 [['Fie'], ['Gaal', 'Gaal Dornick'], 2],
 [['Pirenne', 'Lewis Pirenne'], ['Hardin', 'Salvor Hardin'], 20],
 [['Pirenne', 'Lewis Pirenne'], ['Foundation', 'Second Foundation'], 1],
 [['Emperor'], ['Pirenne', 'Lewis Pirenne'], 2],
 [['Empire', 'Galactic Empire'], ['Hardin', 'Salvor Hardin'], 4],
 [['Emperor'], ['Hardin', 'Salvor Hardin'], 2],
 [['Sutt', 'Jorane Sutt'], ['Fara', 'Jord Fara'], 1],
 [['Fara', 'Jord Fara'], ['Fulham'], 1],
 [['Fulham'], ['Pirenne', 'Lewis Pirenne'], 1],
 [['Dorwin'], ['Empire', 'Galactic Empire'], 2],
 [['Dorwin'], ['Sutt', 'Jorane Sutt'], 1],
 [['Mayor', 'Mayor Hardin'], ['Hardin', 'Salvor Hardin'], 9],
 [['Mayor', 'Mayor Hardin'], ['Sutt', 'Jorane Sutt'], 2],
 [['Hardin', 'Salvor Hardin'], ['Foundation', 'Second Foundation'], 9],
 [['Fara', 'Jord Fara'], ['Seldon', 'Hari Seldon'], 3],
 [['Fara', 'Jord Fara'], ['Hardin', 'Salvor Hardin'], 4],
 [['Hardin', 'Salvor Hardin'], ['dryly'], 1],
 [['Dorwin'], ['Hardin', 'Salvor Hardin'], 2],
 [['Dorwin'], ['Emperor'], 2],
 [['Hardin', 'Salvor Hardin'], ['Fulham'], 1],
 [['Pirenne', 'Lewis Pirenne'], ['Empire', 'Galactic Empire'], 1],
 [['Seldon', 'Hari Seldon'], ['Foundation', 'Second Foundation'], 37],
 [['Pirenne', 'Lewis Pirenne'], ['Dorwin'], 1],
 [['Seldon', 'Hari Seldon'], ['Hardin', 'Salvor Hardin'], 6],
 [['Lee', 'Yohan Lee'], ['Hardin', 'Salvor Hardin'], 10],
 [['Sermak', 'Sef Sermak'], ['Lee', 'Yohan Lee'], 3],
 [['Hardin', 'Salvor Hardin'], ['Sermak', 'Sef Sermak'], 6],
 [['Sermak', 'Sef Sermak'], ['Seldon', 'Hari Seldon'], 2],
 [['Verisof'], ['Mayor', 'Mayor Hardin'], 2],
 [['Wienis'], ['Lepold'], 5],
 [['Verisof'], ['dryly'], 1],
 [['dryly'], ['Wienis'], 1],
 [['Hardin', 'Salvor Hardin'], ['Verisof'], 5],
 [['Seldon', 'Hari Seldon'], ['Plan'], 43],
 [['Plan'], ['Verisof'], 2],
 [['Empire', 'Galactic Empire'], ['Verisof'], 1],
 [['Foundation', 'Second Foundation'], ['Emperor'], 5],
 [['Lepold'], ['Foundation', 'Second Foundation'], 3],
 [['Hardin', 'Salvor Hardin'], ['Wienis'], 14],
 [['Hardin', 'Salvor Hardin'], ['Lepold'], 5],
 [['Foundation', 'Second Foundation'], ['Wienis'], 2],
 [['Sermak', 'Sef Sermak'], ['Bort', 'Lewis Bort'], 3],
 [['Walto'], ['Bort', 'Lewis Bort'], 1],
 [['Bort', 'Lewis Bort'], ['Foundation', 'Second Foundation'], 1],
 [['Hardin', 'Salvor Hardin'], ['Bort', 'Lewis Bort'], 1],
 [['Wienis'], ['Aporat', 'Theo Aporat'], 1],
 [['Foundation', 'Second Foundation'], ['Gorm', 'Les Gorm'], 1],
 [['Capsule'], ['Ponyets', 'Limmar Ponyets'], 1],
 [['Ponyets', 'Limmar Ponyets'], ['Gorm', 'Les Gorm'], 5],
 [['Gorm', 'Les Gorm'], ['Gorov', 'Eskel Gorov'], 1],
 [['Master'], ['Gorov', 'Eskel Gorov'], 1],
 [['Gorov', 'Eskel Gorov'], ['Ponyets', 'Limmar Ponyets'], 10],
 [['Master'], ['Ponyets', 'Limmar Ponyets'], 5],
 [['Sir'], ['Ponyets', 'Limmar Ponyets'], 1],
 [['Gorov', 'Eskel Gorov'], ['Empire', 'Galactic Empire'], 1],
 [['Master'], ['Fie'], 1],
 [['Pherl'], ['Ponyets', 'Limmar Ponyets'], 3],
 [['Pherl'], ['Elders'], 1],
 [['Ponyets', 'Limmar Ponyets'], ['Hardin', 'Salvor Hardin'], 1],
 [['Sutt', 'Jorane Sutt'], ['Mallow', 'Hober Mallow'], 13],
 [['Mallow', 'Hober Mallow'], ['Master'], 5],
 [['Foundation', 'Second Foundation'], ['Mallow', 'Hober Mallow'], 8],
 [['Mallow', 'Hober Mallow'], ['dryly'], 2],
 [['Seldon', 'Hari Seldon'], ['Mallow', 'Hober Mallow'], 6],
 [['Fie'], ['Mallow', 'Hober Mallow'], 2],
 [['Mallow', 'Hober Mallow'], ['Sir'], 2],
 [['Commdor', 'Commdor Asper'], ['Mallow', 'Hober Mallow'], 6],
 [['Foundation', 'Second Foundation'], ['Master'], 2],
 [['Foundation', 'Second Foundation'], ['Commdor', 'Commdor Asper'], 2],
 [['Empire', 'Galactic Empire'], ['Mallow', 'Hober Mallow'], 3],
 [['Mallow', 'Hober Mallow'], ['Barr', 'Ducem Barr'], 4],
 [['Barr', 'Ducem Barr'], ['Empire', 'Galactic Empire'], 7],
 [['Emperor'], ['Barr', 'Ducem Barr'], 5],
 [['Mallow', 'Hober Mallow'], ['Emperor'], 1],
 [['Commdor', 'Commdor Asper'], ['Sutt', 'Jorane Sutt'], 2],
 [['Mallow', 'Hober Mallow'], ['Jael', 'Ankor Jael'], 16],
 [['Jael', 'Ankor Jael'], ['Empire', 'Galactic Empire'], 1],
 [['Jael', 'Ankor Jael'], ['dryly'], 2],
 [['Sutt', 'Jorane Sutt'], ['Jael', 'Ankor Jael'], 1],
 [['Empire', 'Galactic Empire'], ['Sutt', 'Jorane Sutt'], 2],
 [['Seldon', 'Hari Seldon'], ['Sutt', 'Jorane Sutt'], 2],
 [['Empire', 'Galactic Empire'], ['Foundation', 'Second Foundation'], 22],
 [['Empire', 'Galactic Empire'], ['Riose', 'Bel Riose'], 11],
 [['Riose', 'Bel Riose'], ['Barr', 'Ducem Barr'], 21],
 [['Seldon', 'Hari Seldon'], ['Riose', 'Bel Riose'], 2],
 [['Foundation', 'Second Foundation'], ['Riose', 'Bel Riose'], 4],
 [['Riose', 'Bel Riose'], ['Hardin', 'Salvor Hardin'], 1],
 [['Hardin', 'Salvor Hardin'], ['Mallow', 'Hober Mallow'], 4],
 [['Forell', 'Sennett Forell'], ['Fie'], 1],
 [['Forell', 'Sennett Forell'], ['dryly'], 2],
 [['Barr', 'Ducem Barr'], ['Fie'], 1],
 [['Riose', 'Bel Riose'], ['Fie'], 2],
 [['Emperor'], ['Brodrig'], 6],
 [['Riose', 'Bel Riose'], ['Brodrig'], 5],
 [['Brodrig'], ['dryly'], 2],
 [['Emperor'], ['Riose', 'Bel Riose'], 8],
 [['Riose', 'Bel Riose'], ['Devers', 'Lathan Devers'], 7],
 [['Empire', 'Galactic Empire'], ['Devers', 'Lathan Devers'], 2],
 [['Barr', 'Ducem Barr'], ['Foundation', 'Second Foundation'], 7],
 [['Barr', 'Ducem Barr'], ['Devers', 'Lathan Devers'], 12],
 [['Barr', 'Ducem Barr'], ['Brodrig'], 5],
 [['Barr', 'Ducem Barr'], ['dryly'], 1],
 [['Brodrig'], ['Devers', 'Lathan Devers'], 4],
 [['Devers', 'Lathan Devers'], ['Sir'], 1],
 [['Foundation', 'Second Foundation'], ['Devers', 'Lathan Devers'], 4],
 [['Emperor'], ['Devers', 'Lathan Devers'], 4],
 [['Brodrig'], ['Seldon', 'Hari Seldon'], 1],
 [['Forell', 'Sennett Forell'], ['Devers', 'Lathan Devers'], 3],
 [['Barr', 'Ducem Barr'], ['Forell', 'Sennett Forell'], 2],
 [['Seldon', 'Hari Seldon'], ['Fie'], 4],
 [['Emperor'], ['Fie'], 1],
 [['Forell', 'Sennett Forell'], ['Empire', 'Galactic Empire'], 2],
 [['Foundation', 'Second Foundation'], ['Toran', 'Toran Darell'], 9],
 [['Toran', 'Toran Darell'], ['Dad'], 3],
 [['Bayta', 'Bayta Darell'], ['Toran', 'Toran Darell'], 41],
 [['Toran', 'Toran Darell'], ['Fran'], 2],
 [['Fran'], ['Randu'], 3],
 [['Toran', 'Toran Darell'], ['Fie'], 2],
 [['Bayta', 'Bayta Darell'], ['Seldon', 'Hari Seldon'], 4],
 [['Seldon', 'Hari Seldon'], ['Fran'], 1],
 [['Seldon', 'Hari Seldon'], ['Randu'], 3],
 [['Randu'], ['Toran', 'Toran Darell'], 2],
 [['Bayta', 'Bayta Darell'], ['Foundation', 'Second Foundation'], 15],
 [['Devers', 'Lathan Devers'], ['Randu'], 1],
 [['Fran'], ['Devers', 'Lathan Devers'], 2],
 [['Foundation', 'Second Foundation'], ['Fran'], 3],
 [['Randu'], ['Foundation', 'Second Foundation'], 7],
 [['Mule', 'The Mule'], ['Toran', 'Toran Darell'], 12],
 [['Mule', 'The Mule'], ['Randu'], 7],
 [['Fran'], ['Bayta', 'Bayta Darell'], 1],
 [['Mayor', 'Mayor Hardin'], ['Indbur'], 11],
 [['Mayor', 'Mayor Hardin'], ['Foundation', 'Second Foundation'], 1],
 [['Seldon', 'Hari Seldon'], ['Mayor', 'Mayor Hardin'], 1],
 [['Indbur'], ['Foundation', 'Second Foundation'], 4],
 [['Pritcher', 'Han Pritcher'], ['Capsule'], 1],
 [['Toran', 'Toran Darell'], ['dryly'], 1],
 [['Mule', 'The Mule'], ['Bayta', 'Bayta Darell'], 13],
 [['Mule', 'The Mule'], ['Foundation', 'Second Foundation'], 55],
 [['Foundation', 'Second Foundation'],
  ['Magnifico', 'Magnifico Giganticus'],
  2],
 [['Bayta', 'Bayta Darell'], ['Magnifico', 'Magnifico Giganticus'], 25],
 [['Mule', 'The Mule'], ['Magnifico', 'Magnifico Giganticus'], 9],
 [['Magnifico', 'Magnifico Giganticus'], ['Toran', 'Toran Darell'], 12],
 [['Mis', 'Ebling Mis'], ['Indbur'], 8],
 [['Seldon', 'Hari Seldon'], ['Indbur'], 1],
 [['Foundation', 'Second Foundation'], ['Mis', 'Ebling Mis'], 13],
 [['Mis', 'Ebling Mis'], ['dryly'], 2],
 [['dryly'], ['Seldon', 'Hari Seldon'], 1],
 [['Fran'], ['Iwo'], 1],
 [['Mule', 'The Mule'], ['Iwo'], 1],
 [['Mule', 'The Mule'], ['Fie'], 8],
 [['Mule', 'The Mule'], ['Indbur'], 3],
 [['Ovall', 'Ovall Gri'], ['Randu'], 1],
 [['Mule', 'The Mule'], ['Ovall', 'Ovall Gri'], 2],
 [['Mis', 'Ebling Mis'], ['Bayta', 'Bayta Darell'], 9],
 [['Mis', 'Ebling Mis'], ['Magnifico', 'Magnifico Giganticus'], 5],
 [['Mis', 'Ebling Mis'], ['Mayor', 'Mayor Hardin'], 1],
 [['Mallow', 'Hober Mallow'], ['Indbur'], 1],
 [['Mis', 'Ebling Mis'], ['Seldon', 'Hari Seldon'], 3],
 [['Indbur'], ['Randu'], 1],
 [['Toran', 'Toran Darell'], ['Indbur'], 1],
 [['Indbur'], ['Bayta', 'Bayta Darell'], 1],
 [['Mis', 'Ebling Mis'], ['Randu'], 3],
 [['Mule', 'The Mule'], ['Seldon', 'Hari Seldon'], 7],
 [['Mule', 'The Mule'], ['Mis', 'Ebling Mis'], 5],
 [['Pritcher', 'Han Pritcher'], ['Foundation', 'Second Foundation'], 13],
 [['Mule', 'The Mule'], ['Pritcher', 'Han Pritcher'], 16],
 [['Mule', 'The Mule'], ['Fox'], 2],
 [['Indbur'], ['Pritcher', 'Han Pritcher'], 1],
 [['Fox'], ['Fie'], 1],
 [['Mis', 'Ebling Mis'], ['Toran', 'Toran Darell'], 11],
 [['Fie'], ['Foundation', 'Second Foundation'], 5],
 [['Pritcher', 'Han Pritcher'], ['Mis', 'Ebling Mis'], 6],
 [['Mule', 'The Mule'], ['Commason', 'Jord Commason'], 4],
 [['Foundation', 'Second Foundation'], ['Commason', 'Jord Commason'], 3],
 [['Commason', 'Jord Commason'], ['Capsule'], 1],
 [['Commason', 'Jord Commason'], ['Magnifico', 'Magnifico Giganticus'], 1],
 [['Mis', 'Ebling Mis'], ['Fie'], 1],
 [['Pritcher', 'Han Pritcher'], ['Toran', 'Toran Darell'], 2],
 [['Bayta', 'Bayta Darell'], ['Pritcher', 'Han Pritcher'], 5],
 [['Seldon', 'Hari Seldon'], ['Toran', 'Toran Darell'], 1],
 [['Mule', 'The Mule'], ['Empire', 'Galactic Empire'], 6],
 [['Pritcher', 'Han Pritcher'], ['Fie'], 4],
 [['Fie'], ['Sir'], 1],
 [['Sir'], ['Mule', 'The Mule'], 1],
 [['Pritcher', 'Han Pritcher'], ['Sir'], 3],
 [['Channis', 'Bail Channis'], ['Sir'], 2],
 [['Channis', 'Bail Channis'], ['Mule', 'The Mule'], 13],
 [['Foundation', 'Second Foundation'], ['Channis', 'Bail Channis'], 13],
 [['Mule', 'The Mule'], ['dryly'], 1],
 [['dryly'], ['Channis', 'Bail Channis'], 1],
 [['Speaker'], ['Fie'], 5],
 [['Channis', 'Bail Channis'], ['Pritcher', 'Han Pritcher'], 13],
 [['Empire', 'Galactic Empire'], ['Fie'], 1],
 [['Fie'], ['Channis', 'Bail Channis'], 5],
 [['Elders'], ['Channis', 'Bail Channis'], 2],
 [['Elders'], ['Pritcher', 'Han Pritcher'], 1],
 [['Mule', 'The Mule'], ['Elders'], 1],
 [['Mis', 'Ebling Mis'], ['Channis', 'Bail Channis'], 2],
 [['Plan'], ['Empire', 'Galactic Empire'], 5],
 [['Channis', 'Bail Channis'], ['Speaker'], 3],
 [['Mule', 'The Mule'], ['Speaker'], 1],
 [['Speaker'], ['Foundation', 'Second Foundation'], 5],
 [['Bayta', 'Bayta Darell'], ['Darell', 'Arkady Darell'], 6],
 [['Arcadia', 'Arcadia Darell'], ['Darell', 'Arkady Darell'], 17],
 [['Plan'], ['Darell', 'Arkady Darell'], 1],
 [['Plan'], ['Foundation', 'Second Foundation'], 7],
 [['Mallow', 'Hober Mallow'], ['Plan'], 1],
 [['Plan'], ['Fie'], 2],
 [['Anthor', 'Pelleas Anthor'], ['Darell', 'Arkady Darell'], 33],
 [['Toran', 'Toran Darell'], ['Darell', 'Arkady Darell'], 2],
 [['Student'], ['Speaker'], 9],
 [['Plan'], ['Speaker'], 6],
 [['Student'], ['Mule', 'The Mule'], 1],
 [['Foundation', 'Second Foundation'], ['Student'], 1],
 [['Student'], ['Seldon', 'Hari Seldon'], 1],
 [['Turbor', 'Jole Turbor'], ['Semic', 'Elvett Semic'], 3],
 [['Munn', 'Homir Munn'], ['Darell', 'Arkady Darell'], 12],
 [['Anthor', 'Pelleas Anthor'], ['Turbor', 'Jole Turbor'], 3],
 [['Kleise'], ['Munn', 'Homir Munn'], 3],
 [['Foundation', 'Second Foundation'], ['Turbor', 'Jole Turbor'], 4],
 [['Anthor', 'Pelleas Anthor'], ['Munn', 'Homir Munn'], 7],
 [['Kleise'], ['Semic', 'Elvett Semic'], 2],
 [['Kleise'], ['Darell', 'Arkady Darell'], 7],
 [['Darell', 'Arkady Darell'], ['Turbor', 'Jole Turbor'], 2],
 [['Foundation', 'Second Foundation'], ['Semic', 'Elvett Semic'], 2],
 [['Foundation', 'Second Foundation'], ['Kleise'], 1],
 [['Anthor', 'Pelleas Anthor'], ['Foundation', 'Second Foundation'], 10],
 [['Munn', 'Homir Munn'], ['Fie'], 5],
 [['Munn', 'Homir Munn'], ['Arcadia', 'Arcadia Darell'], 4],
 [['Foundation', 'Second Foundation'], ['Munn', 'Homir Munn'], 4],
 [['Mallow', 'Hober Mallow'], ['Devers', 'Lathan Devers'], 1],
 [['Sir'], ['Meirus', 'Lev Meirus'], 1],
 [['Stettin'], ['Meirus', 'Lev Meirus'], 1],
 [['Mule', 'The Mule'], ['Meirus', 'Lev Meirus'], 1],
 [['Foundation', 'Second Foundation'], ['Meirus', 'Lev Meirus'], 3],
 [['Foundation', 'Second Foundation'], ['Stettin'], 5],
 [['Mule', 'The Mule'], ['Plan'], 1],
 [['Munn', 'Homir Munn'], ['Mule', 'The Mule'], 2],
 [['Poochie'], ['Stettin'], 2],
 [['Empire', 'Galactic Empire'], ['Stettin'], 1],
 [['Foundation', 'Second Foundation'], ['Poochie'], 2],
 [['Arcadia', 'Arcadia Darell'], ['Anthor', 'Pelleas Anthor'], 5],
 [['Foundation', 'Second Foundation'], ['Arcadia', 'Arcadia Darell'], 4],
 [['Mule', 'The Mule'], ['Arcadia', 'Arcadia Darell'], 2],
 [['Poochie'], ['Empire', 'Galactic Empire'], 1],
 [['Arcadia', 'Arcadia Darell'], ['Stettin'], 2],
 [['Empire', 'Galactic Empire'], ['Munn', 'Homir Munn'], 1],
 [['Kleise'], ['Anthor', 'Pelleas Anthor'], 1],
 [['Fie'], ['Stettin'], 1],
 [['Mamma'], ['Pappa'], 11],
 [['Pappa'], ['Arcadia', 'Arcadia Darell'], 7],
 [['Pappa'], ['Stettin'], 1],
 [['Arcadia', 'Arcadia Darell'], ['Mamma'], 3],
 [['Arcadia', 'Arcadia Darell'], ['Palver', 'Preem Palver'], 2],
 [['Semic', 'Elvett Semic'], ['Fie'], 3],
 [['Darell', 'Arkady Darell'], ['Fie'], 2],
 [['Semic', 'Elvett Semic'], ['Darell', 'Arkady Darell'], 5],
 [['Anthor', 'Pelleas Anthor'], ['Semic', 'Elvett Semic'], 2],
 [['Mallow', 'Hober Mallow'], ['Darell', 'Arkady Darell'], 1],
 [['Mule', 'The Mule'], ['Darell', 'Arkady Darell'], 1],
 [['Fie'], ['Arcadia', 'Arcadia Darell'], 1],
 [['Anthor', 'Pelleas Anthor'], ['Fie'], 3],
 [['Foundation', 'Second Foundation'], ['Darell', 'Arkady Darell'], 4],
 [['Darell', 'Arkady Darell'], ['Stettin'], 1],
 [['Foundation', 'Second Foundation'], ['Mamma'], 1],
 [['Foundation', 'Second Foundation'], ['Pappa'], 1],
 [['Palver', 'Preem Palver'], ['Pappa'], 1],
 [['Palver', 'Preem Palver'], ['Fie'], 1],
 [['Plan'], ['Turbor', 'Jole Turbor'], 1],
 [['Turbor', 'Jole Turbor'], ['Palver', 'Preem Palver'], 1],
 [['Darell', 'Arkady Darell'], ['Palver', 'Preem Palver'], 1],
 [['Plan'], ['Munn', 'Homir Munn'], 1],
 [['Semic', 'Elvett Semic'], ['Mule', 'The Mule'], 1],
 [['Seldon', 'Hari Seldon'], ['Anthor', 'Pelleas Anthor'], 4],
 [['Munn', 'Homir Munn'], ['Turbor', 'Jole Turbor'], 2],
 [['Munn', 'Homir Munn'], ['Semic', 'Elvett Semic'], 1],
 [['Munn', 'Homir Munn'], ['Seldon', 'Hari Seldon'], 2],
 [['Turbor', 'Jole Turbor'], ['Seldon', 'Hari Seldon'], 1],
 [['Seldon', 'Hari Seldon'], ['Darell', 'Arkady Darell'], 1],
 [['Munn', 'Homir Munn'], ['Stettin'], 1],
 [['Plan'], ['Student'], 1],
 [['Palver', 'Preem Palver'], ['Speaker'], 1]]"""
