"""
Evaluation tags:
PER for person
LOC for location unit
O for no entity.

We add a B- in the beginning of the entity type if this is the beginning of the entity
and a I- if the token represents the continuation of a entity.
Example:
    sentence =      ["Hawking", "was",  "a", "Fellow",  "of",   "the",  "Royal",    "Society"]
    labels_bio =    ["B-per",   "O",    "O", "O",       "O",    "O",    "B-org",    "I-org"]


Precision, Recall, f1-score:
true positives (tp): number of labels of a class that are predicted correctly
false positives (fp): number of predictions of a class that are wrongly predicted
false negatives (fn): number of predictions that predict a class but are not labeled as belonging to the class

PRECISION = tp / (tp + fp)
RECALL = tp / (tp + fn)
F1-SCORE = 2 * ((precision * recall)/(precision + recall))

https://github.com/chakki-works/seqeval
https://stats.stackexchange.com/questions/271980/compute-cohens-kappa-in-multi-label-classification
https://stackoverflow.com/questions/57256287/calculate-kappa-score-for-multi-label-image-classifcation
"""

from config import tqdm
from typing import Dict, Sequence

KEYS = ['start_idx', 'end_idx', 'text', 'type']


def list_of_dicts(list):
    """
    :param list: list of ner entities. The Keys are ['start_idx', 'end_idx', 'text', 'type'] \n E.g: [[0,1, 'Leo Messi', 'PER'], [1,2, 'Armando Maradona', 'PER']]
    :return: list of dictionaries
    """
    dict_list = []
    [dict_list.append(dict(zip(KEYS, elem))) for elem in list]
    return dict_list


def list_of_values(ner_sent, doc):
    """
    :param doc: doc with original words
    :param ner_sent: ner output sentence. E.g:
    doc =       ["Hawking", "was",  "a",    "Fellow",   "of",   "the",  "Royal", "Society"]
    ner_sent =  ["B-PER",   "O",    "O",    "O",        "O", "   O",    "B-ORG", "I-ORG"]
    :return: [[0, 0, 'Hawking', 'PER'], [6, 7, 'Royal Society', 'ORG']]
    """
    list = []
    for idx, token in enumerate(ner_sent):
        if token != 'O':
            if token == 'B-PER' and ner_sent[idx + 1] == 'I-PER':
                list.append([idx, idx + 1, " ".join([doc[idx].text + doc[idx + 1].text]), 'PER'])

            elif token == 'B-PER':
                list.append([idx, idx, doc[idx].text, 'PER'])

            elif token == 'B-LOC' and ner_sent[idx + 1] == 'I-LOC':
                list.append([idx, idx + 1, " ".join([doc[idx].text + doc[idx + 1].text]), 'LOC'])

            elif token == 'B-LOC':
                list.append([idx, idx, doc[idx].text, 'LOC'])
    return list


class Matrics:
    """
    https://towardsdatascience.com/entity-level-evaluation-for-ner-task-c21fb3a8edf
    """

    def __init__(self, sents_true_labels: Sequence[Sequence[Dict]], sents_pred_labels: Sequence[Sequence[Dict]]):
        self.sents_true_labels = sents_true_labels
        self.sents_pred_labels = sents_pred_labels
        self.types = set(entity['type'] for sent in sents_true_labels for entity in sent)
        self.confusion_matrices = {type: {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0} for type in self.types}
        self.scores = {type: {'p': 0, 'r': 0, 'f1': 0} for type in self.types}

    def cal_confusion_matrices(self):
        """Calculate confusion matrices for all sentences."""
        for true_labels, pred_labels in zip(self.sents_true_labels, self.sents_pred_labels):
            for true_label in true_labels:
                entity_type = true_label['type']
                prediction_hit_count = 0
                for pred_label in pred_labels:
                    if pred_label['type'] != entity_type:
                        continue
                    if pred_label['start_idx'] == true_label['start_idx'] and pred_label['end_idx'] == true_label[
                        'end_idx'] and pred_label['text'] == true_label['text']:  # TP
                        self.confusion_matrices[entity_type]['TP'] += 1
                        prediction_hit_count += 1
                    elif ((pred_label['start_idx'] == true_label['start_idx']) or (
                            pred_label['end_idx'] == true_label['end_idx'])) and pred_label['text'] != true_label[
                        'text']:  # boundry error, count FN, FP
                        self.confusion_matrices[entity_type]['FP'] += 1
                        self.confusion_matrices[entity_type]['FN'] += 1
                        prediction_hit_count += 1
                if prediction_hit_count != 1:  # FN, model cannot make a prediction for true_label
                    self.confusion_matrices[entity_type]['FN'] += 1
                prediction_hit_count = 0  # reset to default

    def cal_scores(self):
        """Calculate precision, recall, f1."""
        confusion_matrices = self.confusion_matrices
        scores = {type: {'p': 0, 'r': 0, 'f1': 0} for type in self.types}

        for entity_type, confusion_matrix in confusion_matrices.items():
            if confusion_matrix['TP'] == 0 and confusion_matrix['FP'] == 0:
                scores[entity_type]['p'] = 0
            else:
                scores[entity_type]['p'] = confusion_matrix['TP'] / (confusion_matrix['TP'] + confusion_matrix['FP'])

            if confusion_matrix['TP'] == 0 and confusion_matrix['FN'] == 0:
                scores[entity_type]['r'] = 0
            else:
                scores[entity_type]['r'] = confusion_matrix['TP'] / (confusion_matrix['TP'] + confusion_matrix['FN'])

            if scores[entity_type]['p'] == 0 or scores[entity_type]['r'] == 0:
                scores[entity_type]['f1'] = 0
            else:
                scores[entity_type]['f1'] = 2 * scores[entity_type]['p'] * scores[entity_type]['r'] / (
                        scores[entity_type]['p'] + scores[entity_type]['r'])
        self.scores = scores

    def print_confusion_matrices(self):
        for entity_type, matrix in self.confusion_matrices.items():
            print(f"{entity_type}: {matrix}")

    def print_scores(self):
        for entity_type, score in self.scores.items():
            print(f"{entity_type}: F1-Score: {score['f1']:.4f}, PRECISION: {score['p']:.4f}, RECALL: {score['r']:.4f}")


def y_pred(predicted, parsed_list):
    a = []
    for i in tqdm(range(len(predicted))):
        doc = parsed_list[i]
        ner_sent = predicted[i]
        pre_dict = list_of_values(ner_sent, doc)
        a.append(list_of_dicts(pre_dict))
    return a


def validate():
    # sents_pred_labels = y_pred(predicted, parsed_list)
    matrics = Matrics(sents_true_labels, sents_pred_labels)
    matrics.cal_confusion_matrices()
    matrics.print_confusion_matrices()
    matrics.cal_scores()
    matrics.print_scores()


# region labeled data
sents_pred_labels = [[{'start_idx': 23, 'end_idx': 23, 'text': 'Foundation', 'type': 'PER'}],
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Gorov', 'type': 'PER'},
                      {'start_idx': 22, 'end_idx': 22, 'text': 'Ponyets', 'type': 'PER'},
                      {'start_idx': 33, 'end_idx': 34, 'text': 'Grand Master', 'type': 'PER'}], [], [],
                     [{'start_idx': 4, 'end_idx': 4, 'text': 'Trantor', 'type': 'LOC'}],
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Gaal', 'type': 'PER'},
                      {'start_idx': 22, 'end_idx': 22, 'text': 'Empire', 'type': 'PER'}],
                     [{'start_idx': 1, 'end_idx': 1, 'text': 'Hardin', 'type': 'PER'},
                      {'start_idx': 28, 'end_idx': 28, 'text': 'Terminus', 'type': 'LOC'}],
                     [{'start_idx': 7, 'end_idx': 8, 'text': 'Ebling Mis', 'type': 'PER'},
                      {'start_idx': 12, 'end_idx': 12, 'text': 'Indbur', 'type': 'PER'}],
                     [{'start_idx': 29, 'end_idx': 29, 'text': 'Trantor', 'type': 'LOC'}], [], [],
                     [{'start_idx': 9, 'end_idx': 9, 'text': 'Seldon', 'type': 'PER'}],
                     [{'start_idx': 6, 'end_idx': 6, 'text': 'Board', 'type': 'PER'},
                      {'start_idx': 15, 'end_idx': 15, 'text': 'Emperor', 'type': 'PER'},
                      {'start_idx': 19, 'end_idx': 19, 'text': 'Terminus', 'type': 'LOC'},
                      {'start_idx': 21, 'end_idx': 21, 'text': 'Hardin', 'type': 'PER'}], [], [],
                     [{'start_idx': 1, 'end_idx': 2, 'text': 'Lundin Crast', 'type': 'PER'},
                      {'start_idx': 19, 'end_idx': 19, 'text': 'Foundation', 'type': 'PER'}],
                     [{'start_idx': 72, 'end_idx': 72, 'text': 'Seldon', 'type': 'PER'}],
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Mallow', 'type': 'PER'}],
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Hardin', 'type': 'PER'},
                      {'start_idx': 22, 'end_idx': 22, 'text': 'Board', 'type': 'PER'}], [], [], [],
                     [{'start_idx': 0, 'end_idx': 1, 'text': 'Ducem Barr', 'type': 'PER'}],
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Gaal', 'type': 'PER'},
                      {'start_idx': 88, 'end_idx': 88, 'text': 'Trantor', 'type': 'LOC'}], [],
                     [{'start_idx': 12, 'end_idx': 12, 'text': 'Fara', 'type': 'PER'}], [],
                     [{'start_idx': 0, 'end_idx': 1, 'text': 'LingeChen', 'type': 'PER'},
                      {'start_idx': 13, 'end_idx': 13, 'text': 'Commissioners', 'type': 'PER'},
                      {'start_idx': 28, 'end_idx': 28, 'text': 'Chen', 'type': 'PER'}],
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Hardin', 'type': 'PER'}],
                     [{'start_idx': 38, 'end_idx': 38, 'text': 'Brodrig', 'type': 'PER'}],
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Gaal', 'type': 'PER'}], [], [], [], [], [], [],
                     [{'start_idx': 9, 'end_idx': 9, 'text': 'Bayta', 'type': 'PER'},
                      {'start_idx': 15, 'end_idx': 15, 'text': 'Toran', 'type': 'PER'}],
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Seldon', 'type': 'PER'},
                      {'start_idx': 13, 'end_idx': 13, 'text': 'Fie', 'type': 'PER'}],
                     [{'start_idx': 13, 'end_idx': 13, 'text': 'Trantor', 'type': 'LOC'}],
                     [{'start_idx': 8, 'end_idx': 8, 'text': 'Mule', 'type': 'PER'},
                      {'start_idx': 22, 'end_idx': 22, 'text': 'Empire', 'type': 'PER'},
                      {'start_idx': 38, 'end_idx': 38, 'text': 'Galaxy', 'type': 'PER'},
                      {'start_idx': 63, 'end_idx': 64, 'text': 'Second Empire', 'type': 'PER'}], [],
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Jerril', 'type': 'PER'}],
                     [{'start_idx': 8, 'end_idx': 8, 'text': 'Askonian', 'type': 'PER'}],
                     [{'start_idx': 0, 'end_idx': 1, 'text': 'Haut Rodric', 'type': 'PER'}], [], [], [],
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Mallow', 'type': 'PER'}],
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Arcadia', 'type': 'PER'},
                      {'start_idx': 30, 'end_idx': 30, 'text': 'Trantor', 'type': 'LOC'}]]

sents_true_labels = [[{'start_idx': 18, 'end_idx': 18, 'text': 'Smyrno', 'type': 'LOC'},
                      {'start_idx': 23, 'end_idx': 23, 'text': 'Foundation', 'type': 'LOC'}],  # 0
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Gorov', 'type': 'PER'},
                      {'start_idx': 22, 'end_idx': 22, 'text': 'Ponyets', 'type': 'PER'},
                      {'start_idx': 33, 'end_idx': 34, 'text': 'Grand Master', 'type': 'PER'}],  # 1
                     [],  # 2
                     [],  # 3
                     [{'start_idx': 4, 'end_idx': 4, 'text': 'Trantor', 'type': 'LOC'},
                      {'start_idx': 44, 'end_idx': 45, 'text': 'Galactic center', 'type': 'LOC'}],  # 4
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Gaal', 'type': 'PER'}],  # 5
                     [{'start_idx': 1, 'end_idx': 1, 'text': 'Hardin', 'type': 'PER'},
                      {'start_idx': 17, 'end_idx': 17, 'text': 'Hardin', 'type': 'PER'},
                      {'start_idx': 28, 'end_idx': 28, 'text': 'Terminus', 'type': 'LOC'}],  # 6
                     [{'start_idx': 7, 'end_idx': 8, 'text': 'Ebling Mis', 'type': 'PER'},
                      {'start_idx': 12, 'end_idx': 12, 'text': 'Indbur', 'type': 'PER'}],  # 7
                     [{'start_idx': 7, 'end_idx': 7, 'text': 'Trantor', 'type': 'LOC'},
                      {'start_idx': 29, 'end_idx': 29, 'text': 'Trantor', 'type': 'LOC'}],  # 8
                     [],  # 9
                     [],  # 10
                     [{'start_idx': 9, 'end_idx': 9, 'text': 'Seldon', 'type': 'PER'}],  # 11
                     [{'start_idx': 15, 'end_idx': 15, 'text': 'Emperor', 'type': 'PER'},
                      {'start_idx': 19, 'end_idx': 19, 'text': 'Terminus', 'type': 'LOC'},
                      {'start_idx': 21, 'end_idx': 21, 'text': 'Hardin', 'type': 'PER'}],  # 12
                     [],  # 13
                     [{'start_idx': 1, 'end_idx': 1, 'text': 'Sutt', 'type': 'PER'}],  # 14
                     [{'start_idx': 1, 'end_idx': 2, 'text': 'Lundin Crast', 'type': 'PER'},
                      {'start_idx': 45, 'end_idx': 45, 'text': 'Mayor', 'type': 'PER'}],  # 15
                     [{'start_idx': 0, 'end_idx': 1, 'text': 'The inquisitor', 'type': 'PER'},
                      {'start_idx': 36, 'end_idx': 36, 'text': 'doctor', 'type': 'PER'},
                      {'start_idx': 72, 'end_idx': 72, 'text': 'Seldon', 'type': 'PER'}],  # 16
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Mallow', 'type': 'PER'}],  # 17
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Hardin', 'type': 'PER'},
                      {'start_idx': 17, 'end_idx': 18, 'text': 'Jord Fara', 'type': 'PER'},
                      {'start_idx': 42, 'end_idx': 42, 'text': 'Santanni', 'type': 'PER'}],  # 18
                     [],  # 19
                     [],  # 20
                     [],  # 21
                     [{'start_idx': 0, 'end_idx': 1, 'text': 'Ducem Barr', 'type': 'PER'}],  # 22
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Gaal', 'type': 'PER'},
                      {'start_idx': 88, 'end_idx': 88, 'text': 'Trantor', 'type': 'LOC'}],  # 23
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Suit', 'type': 'PER'}],  # 24
                     [{'start_idx': 12, 'end_idx': 12, 'text': 'Fara', 'type': 'PER'}],  # 25
                     [],  # 26
                     [{'start_idx': 0, 'end_idx': 1, 'text': 'Linge Chen', 'type': 'PER'},
                      {'start_idx': 13, 'end_idx': 13, 'text': 'Commissioners', 'type': 'PER'},
                      {'start_idx': 28, 'end_idx': 28, 'text': 'Chen', 'type': 'PER'}],  # 27
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Hardin', 'type': 'PER'}],  # 28
                     [{'start_idx': 28, 'end_idx': 28, 'text': 'Devers', 'type': 'PER'},
                      {'start_idx': 38, 'end_idx': 38, 'text': 'Brodrig', 'type': 'PER'}],  # 29
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Gaal', 'type': 'PER'}],  # 30
                     [{'start_idx': 2, 'end_idx': 2, 'text': 'patrician', 'type': 'PER'}],  # 31
                     [{'start_idx': 1, 'end_idx': 1, 'text': 'trader', 'type': 'PER'},
                      {'start_idx': 40, 'end_idx': 40, 'text': 'Setdon', 'type': 'PER'}],  # 32
                     [],  # 33
                     [],  # 34
                     [],  # 35
                     [],  # 36
                     [{'start_idx': 9, 'end_idx': 9, 'text': 'Bayta', 'type': 'PER'},
                      {'start_idx': 20, 'end_idx': 20, 'text': 'clown', 'type': 'PER'},
                      {'start_idx': 15, 'end_idx': 15, 'text': 'Toran', 'type': 'PER'}],  # 37
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Seldon', 'type': 'PER'},
                      {'start_idx': 13, 'end_idx': 13, 'text': 'Fie', 'type': 'PER'}],  # 38
                     [{'start_idx': 13, 'end_idx': 13, 'text': 'Trantor', 'type': 'LOC'}],  # 39
                     [{'start_idx': 8, 'end_idx': 8, 'text': 'Mule', 'type': 'PER'},
                      {'start_idx': 22, 'end_idx': 22, 'text': 'Empire', 'type': 'PER'},
                      {'start_idx': 63, 'end_idx': 64, 'text': 'Second Empire', 'type': 'PER'}],  # 40
                     [{'start_idx': 7, 'end_idx': 7, 'text': 'Hardin', 'type': 'PER'}],  # 41
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Jerril', 'type': 'PER'}],  # 42
                     [{'start_idx': 8, 'end_idx': 8, 'text': 'Askonian', 'type': 'PER'}],  # 43
                     [{'start_idx': 0, 'end_idx': 1, 'text': 'Haut Rodric', 'type': 'PER'}],  # 44
                     [],  # 45
                     [],  # 46
                     [],  # 47
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Mallow', 'type': 'PER'}],  # 48
                     [{'start_idx': 0, 'end_idx': 0, 'text': 'Arcadia', 'type': 'PER'},
                      {'start_idx': 30, 'end_idx': 30, 'text': 'Trantor', 'type': 'LOC'}]]  # 49
# endregion


def visualize_ner(ydx):
    from preprocess import get_texts
    from config import spacy, FoundationTrilogy, displacy
    from utils import read_list
    from spacy.tokens import Span

    validation_idx = read_list('validation_dataset')
    sentences2 = get_texts(FoundationTrilogy)
    sentences = [sentences2[i] for i in validation_idx]
    nlp2 = spacy.load("en_core_web_sm", disable=['ner'])

    doc = nlp2(sentences[ydx])

    spans = []
    for sp in sents_pred_labels[ydx]:
        spans.append(Span(doc, int(sp['start_idx']), int(sp['end_idx']+1), label=sp['type']))

    doc.ents = spans
    colors = {"PER": "linear-gradient(90deg, #aa9cfc, #fc9ce7)", "LOC": "linear-gradient(90deg, #aa9cfc, #fc9ce7)"}
    options = {"ents": ["PER", "LOC"], "colors": colors}
    displacy.serve(doc, style="ent", options=options)
    # go to http://localhost:5000/


if __name__ == '__main__':
    validate()
    # visualize_ner(23)
