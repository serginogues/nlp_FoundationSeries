"""
Soft TF-IDF
https://hpi.de/fileadmin/user_upload/fachgebiete/naumann/folien/SS13/DPDC/DPDC_12_Similarity.pdf
https://github.com/kvpradap/py_stringmatching
https://python.hotexamples.com/es/examples/py_stringmatching.utils/-/sim_check_for_none/python-sim_check_for_none-function-examples.html
"""
from config import combinations
from utils import is_name, write_list, read_list
import collections
import math


def normalize_list(entity_list, STAGE=True):
    print("Start NORMALIZATION")
    if STAGE:
        normalized = []
        copy_list = entity_list.copy()
        for a, b in combinations(entity_list, 2):

            val = (monge_elkan(a.split(" "), b.split(" ")) + monge_elkan(b.split(" "), a.split(" "))) / 2
            if val > 0.81:
                lis = [i for i, pair in enumerate(normalized) for name in pair for w in name.split(" ") if
                       w == a or w == b]
                if len(lis) > 0:
                    i = lis[0]
                    normalized[i].append(a)
                    normalized[i].append(b)
                    normalized[i] = list(set(normalized[i]))
                else:
                    normalized.append([a, b])
                if a in copy_list:
                    copy_list.remove(a)
                if b in copy_list:
                    copy_list.remove(b)

        # Do a second normalization of entities sharing surname
        [normalized.append([ent]) for ent in copy_list]

        """# if unclassified contains words in normalized, add it to tuple
        for i, tu in enumerate(normalized):
            for w in tu:
                a = [x for x in unclassified if is_name(x, w) and 0.81 < (
                        (monge_elkan(w.split(" "), x.split(" ")) + monge_elkan(x.split(" "), w.split(" "))) / 2)]
                if len(a) > 0:
                    [normalized[i].append(x) for x in a]

        for i, ent in enumerate(unclassified):
            c = ent.split(" ")
            if len(c) == 2:
                a = [w for x in normalized for w in x if w == c[0] and len(x) == 1]
                b = [w for x in normalized for w in x if w == c[1] and len(x) == 1]
                if a and b:
                    [normalized.remove(x) for x in normalized if x[0] == a[0]]
                    [normalized.remove(x) for x in normalized if x[0] == b[0]]
                    normalized.append([ent, a[0], b[0]])"""

        for a, b in combinations([[i, x] for i, x in enumerate(normalized) if len(x) == 1], 2):
            if a[1][0] in b[1][0] or b[1][0] in a[1][0]:
                [normalized.remove(x) for x in normalized if x[0] == a[1][0]]
                [normalized.remove(x) for x in normalized if x[0] == b[1][0]]
                normalized.append([a[1][0], a[1][0]])
                normalized[-1] = list(set(normalized[-1]))

        [normalized[i].remove(w) for i, x in enumerate(normalized) for w in x if w == 'Seldon']
        [normalized[i].append('Seldon') for i, x in enumerate(normalized) if x[0] == 'Hari Seldon']
        write_list('normalized', normalized)

    else:
        normalized = read_list('normalized')

    print("NER and NORMALIZATION finished:", len(normalized), "'person' entities found")
    return normalized


class Similarity:
    def __init__(self, string1, string2, score):
        self.first_string = string1
        self.second_string = string2
        self.similarity_score = score


def jaro(string1, string2):
    """
    Computes the Jaro measure between two strings.
    The Jaro measure is a type of edit distance, This was developed mainly to compare short strings,
    such as first and last names.
    Args:
        string1,string2 (str): Input strings
    Returns:
        Jaro measure (float)
    Examples:
        jaro('MARTHA', 'MARHTA')
        0.9444444444444445
        jaro('DWAYNE', 'DUANE')
        0.8222222222222223
        jaro('DIXON', 'DICKSONX')
        0.7666666666666666
    """

    len_s1 = len(string1)
    len_s2 = len(string2)

    max_len = max(len_s1, len_s2)
    search_range = (max_len // 2) - 1
    if search_range < 0:
        search_range = 0

    flags_s1 = [False] * len_s1
    flags_s2 = [False] * len_s2

    common_chars = 0
    for i, ch_s1 in enumerate(string1):
        low = i - search_range if i > search_range else 0
        hi = i + search_range if i + search_range < len_s2 else len_s2 - 1
        for j in range(low, hi + 1):
            if not flags_s2[j] and string2[j] == ch_s1:
                flags_s1[i] = flags_s2[j] = True
                common_chars += 1
                break
    if not common_chars:
        return 0
    k = trans_count = 0
    for i, f_s1 in enumerate(flags_s1):
        if f_s1:
            for j in range(k, len_s2):
                if flags_s2[j]:
                    k = j + 1
                    break
            if string1[i] != string2[j]:
                trans_count += 1
    trans_count /= 2
    common_chars = float(common_chars)
    weight = ((common_chars / len_s1 + common_chars / len_s2 +
               (common_chars - trans_count) / common_chars)) / 3
    return weight


def monge_elkan(bag1, bag2, sim_func=jaro):
    """
    Compute Monge-Elkan similarity measure between two bags (lists).

    The Monge-Elkan similarity measure is a type of Hybrid similarity measure that combine the benefits of
    sequence-based and set-based methods. This can be effective for domains in which more control is needed
    over the similarity measure. It implicitly uses a secondary similarity measure, such as levenshtein to compute
    over all similarity score.

    Args:
        bag1,bag2 (list): Input lists

        sim_func (function): Secondary similarity function. This is expected to be a sequence-based
            similarity measure (defaults to levenshtein)

    Returns:
        Monge-Elkan similarity score (float)

    Examples:
        monge_elkan(['Niall'], ['Neal'])
        0.8049999999999999
        monge_elkan(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'], ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'])
        0.8677218614718616
        monge_elkan(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'], ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'], sim_func=needleman_wunsch)
        2.0
        monge_elkan(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'], ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'], sim_func=affine)
        2.25
        monge_elkan([''], ['a'])
        0.0
        monge_elkan(['Niall'], ['Nigel'])
        0.7866666666666667

    References:
        * Principles of Data Integration book
    """

    # aggregated sum of all the max sim score of all the elements in bag1
    # with elements in bag2
    sum_of_maxes = 0
    for t1 in bag1:
        max_sim = float('-inf')
        for t2 in bag2:
            max_sim = max(max_sim, sim_func(t1, t2))
        sum_of_maxes += max_sim
    sim = float(sum_of_maxes) / float(len(bag1))
    return sim


def soft_tfidf(bag1, bag2, corpus_list=None, sim_func=jaro, threshold=0.5):
    """
    Compute Soft-tfidf measures between two lists given the corpus information.

    Args:
        bag1,bag2 (list): Input lists

        corpus_list (list of lists): Corpus list (default is set to None) of strings. If set to None,
            the input list are considered the only corpus

        sim_func (func): Secondary similarity function. This should return a similarity score between two strings (optional),
            default is jaro similarity measure

        threshold (float): Threshold value for the secondary similarity function (defaults to 0.5). If the similarity
            of a token pair exceeds the threshold, then the token pair is considered a match.

    Returns:
        Soft TF-IDF measure between the input lists

    Raises:
        TypeError : If the inputs are not lists or if one of the inputs is None.

    Examples:
        soft_tfidf(['a', 'b', 'a'], ['a', 'c'], [['a', 'b', 'a'], ['a', 'c'], ['a']], sim_func=jaro, threshold=0.8)
        0.17541160386140586
        soft_tfidf(['a', 'b', 'a'], ['a'], [['a', 'b', 'a'], ['a', 'c'], ['a']], threshold=0.9)
        0.5547001962252291
        soft_tfidf(['a', 'b', 'a'], ['a'], [['x', 'y'], ['w'], ['q']])
        0.0
        soft_tfidf(['aa', 'bb', 'a'], ['ab', 'ba'], sim_func=affine, threshold=0.6)
        0.81649658092772592

    References:
        * Principles of Data Integration book
    """
    # if corpus is not provided treat input string as corpus
    if corpus_list is None:
        corpus_list = [bag1, bag2]
    corpus_size = len(corpus_list) * 1.0
    # term frequency for input strings
    tf_x, tf_y = collections.Counter(bag1), collections.Counter(bag2)
    # number of documents an element appeared
    element_freq = {}
    # set of unique element
    total_unique_elements = set()
    for document in corpus_list:
        temp_set = set()
        for element in document:
            # adding element only if it is present in one of two input string
            if element in bag1 or element in bag2:
                temp_set.add(element)
                total_unique_elements.add(element)
        # update element document frequency for this document
        for element in temp_set:
            element_freq[element] = element_freq[element] + 1 if element in element_freq else 1
    similarity_map = {}
    # calculating the term sim score against the input string 2, construct similarity map
    for x in bag1:
        if x not in similarity_map:
            max_score = 0.0
            for y in bag2:
                score = sim_func(x, y)
                # adding sim only if it is above threshold and highest for this element
                if score > threshold and score > max_score:
                    similarity_map[x] = Similarity(x, y, score)
                    max_score = score
    result, v_x_2, v_y_2 = 0.0, 0.0, 0.0
    # soft-tfidf calculation
    for element in total_unique_elements:
        # numerator
        if element in similarity_map:
            sim = similarity_map[element]
            idf_first = corpus_size if sim.first_string not in element_freq else corpus_size / \
                                                                                 element_freq[sim.first_string]
            idf_second = corpus_size if sim.second_string not in element_freq else corpus_size / \
                                                                                   element_freq[sim.second_string]
            v_x = 0 if sim.first_string not in tf_x else idf_first * tf_x[sim.first_string]
            v_y = 0 if sim.second_string not in tf_y else idf_second * tf_y[sim.second_string]
            result += v_x * v_y * sim.similarity_score
        # denominator
        idf = corpus_size if element not in element_freq else corpus_size / element_freq[element]
        v_x = 0 if element not in tf_x else idf * tf_x[element]
        v_x_2 += v_x * v_x
        v_y = 0 if element not in tf_y else idf * tf_y[element]
        v_y_2 += v_y * v_y
    return result if v_x_2 == 0 else result / (math.sqrt(v_x_2) * math.sqrt(v_y_2))
