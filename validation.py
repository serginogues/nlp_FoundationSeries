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
#TODO: For rules based approaches you will have false positives and false negatives.
# You can measure this by taking a random subset and express the quality in precision, recall, f1, etc.
from seqeval.metrics import precision_score, recall_score, f1_score, classification_report

sentence = ["Hawking", "was", "a", "Fellow", "of", "the", "Royal", "Society", ",", "a", "lifetime", "member",
            "of", "the", "Pontifical", "Academy", "of", "Sciences", ",", "and", "a", "recipient", "of",
            "the", "Presidential", "Medal", "of", "Freedom", ",", "the", "highest", "civilian", "award",
            "in", "the", "United", "States", "."]

y_true = [["B-PER", "O", "O", "O", "O", "O", "B-ORG", "I-ORG", "O", "O", "O", "O", "O", "O",
              "B-ORG", "I-ORG", "I-ORG", "I-ORG", "O", "O", "O", "O", "O", "O", "O", "O", "O",
              "O", "O", "O", "O", "O", "O", "O", "O", "B-GEO", "I-GEO", "O"]]

y_pred = [["B-PER", "O", "O", "O", "O", "O", "B-ORG", "B-ORG", "O", "O", "O", "O", "O",
                "O", "B-ORG", "I-ORG", "B-ORG", "I-ORG", "O", "O", "O", "O", "O", "O", "O",
                "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "B-GEO", "I-GEO", "O"]]
print(precision_score(y_true, y_pred))
print(recall_score(y_true, y_pred))
print(f1_score(y_true, y_pred))
print(classification_report(y_true, y_pred))
