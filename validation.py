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
# TODO: For rules based approaches you will have false positives and false negatives.
# You can measure this by taking a random subset and express the quality in precision, recall, f1, etc.
from config import tqdm
from seqeval.metrics import precision_score, recall_score, f1_score, classification_report
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
                list.append([idx, idx+1, " ".join([doc[idx].text + doc[idx+1].text]), 'PER'])

            elif token == 'B-PER':
                list.append([idx, idx, doc[idx].text, 'PER'])

            elif token == 'B-LOC' and ner_sent[idx + 1] == 'I-LOC':
                list.append([idx, idx+1, " ".join([doc[idx].text + doc[idx+1].text]), 'LOC'])

            elif token == 'B-LOC':
                list.append([idx, idx, doc[idx].text, 'LOC'])
    return list


class Matrics:
    """
    Ignores entity type
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


def validate(predicted, parsed_list):
    sents_pred_labels = y_pred(predicted, parsed_list)
    matrics = Matrics(sents_true_labels, sents_pred_labels)
    matrics.cal_confusion_matrices()
    matrics.print_confusion_matrices()
    matrics.cal_scores()
    matrics.print_scores()


sents_true_labels = [[{'start_idx': 0, 'end_idx': 1, 'text': 'Foreign Ministry', 'type': 'LOC'},
                      {'start_idx': 3, 'end_idx': 4, 'text': 'Shen Guofang', 'type': 'PER'},
                      {'start_idx': 6, 'end_idx': 6, 'text': 'Reuters', 'type': 'ORG'}]]

"""sents_pred_labels = [[{'start_idx': 3, 'end_idx': 3, 'text': 'Shen', 'type': 'PER'},
                      {'start_idx': 6, 'end_idx': 6, 'text': 'Reuters', 'type': 'ORG'}]]"""


