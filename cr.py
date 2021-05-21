"""
Coreference resolution model
Unification of Character Occurrences (alias resolution): grouping proper nouns referring to the same character
https://github.com/huggingface/neuralcoref
"""
from config import nlp


def predict(doc):
    return doc._.coref_resolved, doc._.coref_clusters


"""def predict(text):
    pred = predictor.predict(text)
    clusters = pred['clusters']
    document = pred['document']

    clust = []
    for cluster in clusters:
        list = []
        for range in cluster:
            if range[0] == range[1]:
                list.append([document[range[0]], range[0]])
            else:
                list.append([" ".join(document[range[0]:range[1]]), range])
        clust.append(list)
    # solved = predictor.coref_resolved(text)
    return [], clust"""


"""def get_clusters(text):
    # https://code.likeagirl.io/obtaining-allennlp-coreference-resolution-readable-clusters-in-python-37cd964d6ca0
    pred = predictor.predict(text)
    clusters = pred['clusters']
    document = pred['document']

    n = 0
    doc = {}
    for obj in document:
        doc.update({n :  obj})  # create a dictionary of each word with its respective index, making it easier later.
        n = n+1

    clus_all = []
    cluster = []
    for i in range(0, len(clusters)):
        one_cl = clusters[i]
        for count in range(0, len(one_cl)):
            obj = one_cl[count]
            for num in range((obj[0]), (obj[1]+1)):
                for n in doc:
                    if num == n:
                        cluster.append(doc[n])
        clus_all.append(cluster)
        cluster = []

    return clus_all"""


"""def find_events(text, entity, entity_list):
    
    # Find information about an entity in the text
    
    cr_text = predict(text)
    clusters = get_clusters(text)
    cr_doc = nlp(cr_text)

    events = []
    #TODO: Solve case when there is more than one entity
    idx_token = [i for i, tok in enumerate(cr_doc) if entity_from_token([entity], tok.text)]
    for i, token in enumerate(cr_doc):
        if i in idx_token:
            if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
                dobj = [x for x in token.head.children if x.dep_ == "dobj"]
                if len(dobj) > 0:
                    dobj = dobj[0]
                    verb = token.head.text

                    list = [clust for clust in clusters for noun in clust if dobj.text == noun]
                    if any(list):
                        dobj_ent = [x for ent in list[0] for x in entity_from_token(entity_list, ent) if len(ent) > 2]
                        if any(dobj_ent) and dobj_ent[0] != entity:
                            dobj = dobj_ent[0]
                            events.append((entity[0], verb, dobj))
    return events"""
