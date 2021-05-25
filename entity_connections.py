"""
Given a text and a list of entities (post NER) find all connections between them
"""
from config import combinations, tqdm
from utils import read_list, write_list


def alias_resolution(list):
    if any(list):
        return list[0]
    else:
        return None


def family_links(entity_list, connection_list):
    """
    family connections by surname \n
    :return: List of connected entities by surname
    """

    for subset in combinations(entity_list, 2):
        name1 = str(subset[0][0]).split(" ")
        name2 = str(subset[1][0]).split(" ")
        if len(name1) > 1 and len(name2) > 1 and name1[1] == name2[1]:
            connection_list.append([subset[0], subset[1], 1])

    return connection_list


def link_two_person(connection_list, entity1, entity):
    """
    Creates link betweeen two entities if conditions apply
    :returns: new link list
    """
    if entity1 != entity:
        found = False
        for link in connection_list:
            a = False
            b = False
            for i, ent in enumerate(link):
                if i != 2 and entity1 == ent:
                    a = True
                if i != 2 and entity == ent:
                    b = True
            if a and b:
                link[2] += 1
                found = True

        if not found:
            connection_list.append([entity1, entity, 1])

    return connection_list


def LINK_ENTITIES(parsed_list, predicted, STAGE=True):
    """
    Two entities are considered to have a link if they appear in a range of two consecutive sentences.
    :return: a list of tuples
    """
    print("Start LINKS")
    if STAGE:
        people_links = []
        per_link = []
        location_links = []
        events = []

        for idx in tqdm(range(len(parsed_list))):
            per, loc, per_idx, loc_idx = get_ents_from_predicted(predicted[idx], parsed_list[idx])

            # CR per sentence
            if len(per_idx)>1:
                ev = coref_events(parsed_list[idx], per_idx, loc_idx)
                if any(ev):
                    [x.append(idx) for x in ev]
                    events.append([x for x in ev])


            # PER + LOC LINKS per two sentences
            if idx < len(parsed_list) - 1:
                per2, loc2, per_idx2, loc_idx2 = get_ents_from_predicted(predicted[idx+1], parsed_list[idx+1])
                per += per2
                loc += loc2
                per_idx += per_idx2
                loc_idx += loc_idx2
            per = list(set(per))
            loc = list(set(loc))

            # PEOPLE
            for a, b in combinations(per, 2):
                link_two_person(people_links, a, b)
                per_link.append([a, b, idx])

            # LOCATIONS
            if any(loc) and any(per):
                for l in loc:
                    for p in per:
                        if p != l:
                            location_links.append([l, p, idx])

        # POST PROCESS
        people_links = sorted([x for x in people_links if x[2] > 4], key=lambda x: x[2], reverse=True)
        events = [x[0] for x in events]
        write_list('people_links', people_links)
        write_list('location_links', location_links)
        write_list('events', events)

    else:
        people_links = read_list('people_links')
        location_links = read_list('location_links')
    return people_links, location_links, events


def coref_events(doc, per_idx, loc_idx):
    facts = []
    from config import displacy
    with open('doc_dep.html', 'w') as f:
        f.write(displacy.render(doc, style="dep", options=dict(compact=True)))
    # 0 - get PER and LOC entities and references
    per = [get_token_list_from_cluster(doc[i], doc) for i in per_idx]
    loc = [get_token_list_from_cluster(doc[i], doc) for i in loc_idx]

    # 1 - get all nsubj and dobj and compare them
    per_dobj = [token for token in doc if token.dep_ == "dobj"]
    per_nsubj = [token for token in doc if token.dep_ == "nsubj"]
    # 2 - get events
    events = [[a, a.head.text, b] for a in per_dobj for b in per_nsubj if b.head == a.head and a.head.pos_ == 'VERB']
    if len(events) > 0:
        # 3 - check if any entity or its mentions in events
        for event in events:
            solved = False
            dobj, nsubj = None, None
            for i, ref in enumerate(per):
                a = [x for x in ref if x == event[0]]
                b = [x for x in ref if x == event[2]]
                if any(a):
                    dobj = ref[0]
                if any(b):
                    nsubj = ref[0]
            if dobj != None and nsubj != None and dobj != nsubj:
                event[0] = dobj.text
                event[2] = nsubj.text
                facts.append(event)
            else:
                for i, ref in enumerate(loc):
                    a = [x for x in ref if x == event[0]]
                    b = [x for x in ref if x == event[2]]
                    if any(a):
                        dobj = ref[0]
                    if any(b):
                        nsubj = ref[0]
                if dobj != None and nsubj != None and dobj != nsubj:
                    event[0] = dobj.text
                    event[2] = nsubj.text
                    facts.append(event)

    return facts


def get_token_list_from_cluster(token, doc):
    tokens = [token]
    if token._.in_coref:
        cluster = [x for x in token._.coref_clusters][0]
        for span in cluster:
            if span.start+1 == span.end:
                tok = doc[span.start]
                if tok != token:
                    tokens.append(tok)
            else:
                l = doc[span.start:span.end]
                for tok in l:
                    if tok != token:
                        tokens.append(tok)
    return tokens


def get_ents_from_predicted(y_pred, doc):
    """
    :param predicted: ner output
    :param doc: spacy doc
    :return:
    """
    per = []
    loc = []
    per_idx = []
    loc_idx = []
    for i, name in [(i, tag) for i, tag in enumerate(y_pred) if tag != 'O']:
        if name == 'B-PER':
            per.append(doc[i].text)
            per_idx.append(i)
        elif name == 'I-PER':
            per[-1] = " ".join([per[-1], doc[i].text])
            per_idx[-1] = i
        if name == 'B-LOC':
            loc.append(doc[i].text)
            loc_idx.append(i)
        elif name == 'I-LOC':
            loc[-1] = " ".join([loc[-1], doc[i].text])
            loc_idx[-1] = i

    return per, loc, per_idx, loc_idx


