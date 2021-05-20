"""
Given a text and a list of entities (post NER) find all connections between them
"""
from config import combinations
from utils import get_ents_from_doc, pairwise


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


def link_entities(connection_list, entity1, entity):
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


def entity_links(entity_list, parsed_list, STAGE=False):
    """
    Two entities are considered to have a link if they appear in a range of two consecutive sentences.
    :return: a list of tuples
    """
    if STAGE:
        connection_list = []
        # connection_list = family_links(entity_list, connection_list)
        for pair in pairwise(parsed_list):
            ents_list = get_ents_from_doc(pair[0]) + get_ents_from_doc(pair[1])
            ents_list = list(set(ents_list))
            if any(ents_list):
                # get list of person entities from ents_list
                candidates = get_candidates(ents_list, entity_list)
                for a, b in combinations(candidates, 2):
                    connection_list = link_entities(connection_list, a, b)

        connection_list = sorted([x for x in connection_list if x[2]>2], key=lambda x: x[2], reverse=True)
    else:
        connection_list = [['Second Foundation', 'Mule', 154],
                           ['Second Foundation', 'Hari Seldon', 136],
                           ['First', 'Second Foundation', 90],
                           ['First', 'First Speaker', 89],
                           ['Toran', 'Bayta', 81],
                           ['Second Foundation', 'Empire', 74],
                           ['Hari Seldon', 'Empire', 58],
                           ['Seldon Historical', 'Hari Seldon', 57],
                           ['Magnifico', 'Bayta', 54],
                           ['Darell', 'Anthor', 51],
                           ['Channis', 'Mule', 49],
                           ['Twice Pritcher', 'Mule', 43],
                           ['Channis', 'Second Foundation', 43],
                           ['Hardin', 'Second Foundation', 42],
                           ['Magnifico', 'Toran', 41],
                           ['Hari Seldon', 'Gaal Dornick', 39],
                           ['First', 'Mule', 38],
                           ['Channis', 'Twice Pritcher', 38],
                           ['Twice Pritcher', 'Second Foundation', 36],
                           ['Bayta', 'Mule', 35],
                           ['Magnifico', 'Mule', 34],
                           ['Homir', 'Munn', 34],
                           ['Second Foundation', 'Flober Mallow', 33],
                           ['Twice Pritcher', 'Han', 33],
                           ['Mis', 'Second Foundation', 33],
                           ['Arcadia', 'Darell', 33],
                           ['First', 'Empire', 32],
                           ['Toran', 'Mule', 32],
                           ['Hari Seldon', 'Mule', 31],
                           ['Jael', 'Flober Mallow', 29],
                           ['Toran', 'Second Foundation', 29],
                           ['Pirenne', 'Hardin', 28],
                           ['Mis', 'Toran', 27],
                           ['First', 'Hari Seldon', 26],
                           ['Hardin', 'Senter', 25],
                           ['Hardin', 'Wienis', 25],
                           ['Bayta', 'Second Foundation', 25],
                           ['Fie', 'Second Foundation', 25],
                           ['Mis', 'Mule', 25],
                           ['Twice Pritcher', 'Flan', 24],
                           ['Mis', 'Bayta', 24],
                           ['Mis', 'Indbur', 23],
                           ['Mamma', 'Pappa', 23],
                           ['Magnifico', 'Mis', 22],
                           ['Munn', 'Darell', 22],
                           ['Emperor', 'Empire', 21],
                           ['Haven', 'Second Foundation', 21],
                           ['First', 'Channis', 21],
                           ['Arcadia', 'Callia', 21],
                           ['Hardin', 'Hari Seldon', 20],
                           ['Sermak', 'Hardin', 20],
                           ['Fie', 'Mule', 20],
                           ['Anthor', 'Munn', 20],
                           ['Munn', 'Second Foundation', 19],
                           ['Anthor', 'Second Foundation', 19],
                           ['Board', 'Hardin', 18],
                           ['Riose', 'Bel', 18],
                           ['Riose', 'Barr', 18],
                           ['Brodrig', 'Emperor', 18],
                           ['Randu', 'Mule', 18],
                           ['Darell', 'Kleise', 18],
                           ['Arcadia', 'Munn', 18],
                           ['Korell', 'Second Foundation', 17],
                           ['Haven', 'Mule', 17],
                           ['Homir', 'Second Foundation', 17],
                           ['Verisof', 'Hardin', 16],
                           ['Seldon Historical', 'Second Foundation', 16],
                           ['Empire', 'Mule', 16],
                           ['First', 'Student', 16],
                           ['Darell', 'Second Foundation', 16],
                           ['Arcadia', 'Pappa', 16],
                           ['Barr', 'Empire', 15],
                           ['Hardin', 'Flober Mallow', 15],
                           ['Barr', 'Second Foundation', 15],
                           ['Flan', 'Second Foundation', 15],
                           ['Munn', 'Mule', 15],
                           ['Stettin', 'Second Foundation', 15],
                           ['Stettin', 'Callia', 15],
                           ['Hari Seldon', 'Emperor', 14],
                           ['Hari Seldon', 'Flober Mallow', 14],
                           ['Randu', 'Second Foundation', 14],
                           ['Mis', 'Twice Pritcher', 14],
                           ['First Speaker', 'Student', 14],
                           ['Semic', 'Darell', 14],
                           ['Turbor', 'Darell', 14],
                           ['Arcadia', 'Homir', 14],
                           ['Board', 'Pirenne', 13],
                           ['Hardin', 'Dorwin', 13],
                           ['Barr', 'Emperor', 13],
                           ['Korell', 'Flober Mallow', 13],
                           ['Riose', 'Emperor', 13],
                           ['Bayta', 'Twice Pritcher', 13],
                           ['First Speaker', 'Mule', 13],
                           ['Arcadia', 'Second Foundation', 13],
                           ['Lepold', 'Wienis', 12],
                           ['Twer', 'Flober Mallow', 12],
                           ['Riose', 'Empire', 12],
                           ['Second Foundation', 'Indbur', 12],
                           ['Mis', 'Hari Seldon', 12],
                           ['End', 'Star', 12],
                           ['First Speaker', 'Channis', 12],
                           ['First Speaker', 'Second Foundation', 12],
                           ['Fie', 'Hari Seldon', 11],
                           ['Lepold', 'Second Foundation', 11],
                           ['Master', 'Second Foundation', 11],
                           ['Pherl', 'Master', 11],
                           ['Haven', 'Bayta', 11],
                           ['Bayta', 'Hari Seldon', 11],
                           ['Channis', 'Fie', 11],
                           ['Turbor', 'Munn', 11],
                           ['Turbor', 'Second Foundation', 11],
                           ['Hari Seldon', 'Star', 10],
                           ['Sermak', 'Senter', 10],
                           ['Second Foundation', 'Wienis', 10],
                           ['Lepold', 'Hardin', 10],
                           ['Riose', 'Second Foundation', 10],
                           ['Indbur', 'Mule', 10],
                           ['Bayta', 'Darell', 10],
                           ['Homir', 'Stettin', 10],
                           ['Arcadia', 'Mule', 10],
                           ['Hardin', 'Emperor', 9],
                           ['Empire', 'Hardin', 9],
                           ['Hardin', 'Star', 9],
                           ['Toran', 'Dad', 9],
                           ['Randu', 'Flan', 9],
                           ['Twice Pritcher', 'Fie', 9],
                           ['Arcadia', 'Hari Seldon', 9],
                           ['Arcadia', 'Anthor', 9],
                           ['Poochie', 'Callia', 9],
                           ['Board', 'Emperor', 8],
                           ['Haut Rodric', 'Hardin', 8],
                           ['Pirenne', 'Haut Rodric', 8],
                           ['Second Foundation', 'Star', 8],
                           ['Ponyets', 'Master', 8],
                           ['Master', 'Flober Mallow', 8],
                           ['Barr', 'Brodrig', 8],
                           ['Barr', 'Hari Seldon', 8],
                           ['Korell', 'Barr', 8],
                           ['Toran', 'Twice Pritcher', 8],
                           ['Randu', 'Mangin', 8],
                           ['Haven', 'Randu', 8],
                           ['Seldon Historical', 'Mule', 8],
                           ['Homir', 'Darell', 8],
                           ['First', 'Callia', 8],
                           ['Homir', 'Mule', 8],
                           ['Semic', 'Anthor', 8],
                           ['Commissioner', 'Hari Seldon', 7],
                           ['Board', 'Second Foundation', 7],
                           ['Pirenne', 'Second Foundation', 7],
                           ['Commissioner', 'Second Foundation', 7],
                           ['Second Foundation', 'Emperor', 7],
                           ['Ponyets', 'Gorov', 7],
                           ['Master', 'Gorov', 7],
                           ['Space', 'Second Foundation', 7],
                           ['Riose', 'Hari Seldon', 7],
                           ['Flan', 'Mule', 7],
                           ['Darell', 'Mule', 7],
                           ['Semic', 'Turbor', 7],
                           ['Semic', 'Munn', 7],
                           ['Stettin', 'Mule', 7],
                           ['Stettin', 'First', 7],
                           ['Fie', 'Munn', 7],
                           ['Callia', 'Second Foundation', 7],
                           ['Hari Seldon', 'Munn', 7],
                           ['Homir', 'Callia', 7],
                           ['Stettin', 'Munn', 7],
                           ['Avakim', 'Gaal Dornick', 6],
                           ['Pirenne', 'Emperor', 6],
                           ['Hari Seldon', 'Senter', 6],
                           ['Verisof', 'Second Foundation', 6],
                           ['Sermak', 'Bort', 6],
                           ['Star', 'Flober Mallow', 6],
                           ['Fie', 'Flober Mallow', 6],
                           ['Barr', 'Flober Mallow', 6],
                           ['Bel', 'Empire', 6],
                           ['Riose', 'Siwennian', 6],
                           ['Barr', 'Siwennian', 6],
                           ['Toran', 'Hari Seldon', 6],
                           ['Hari Seldon', 'Indbur', 6],
                           ['Magnifico', 'Second Foundation', 6],
                           ['Mis', 'Randu', 6],
                           ['Arcadia', 'Seldon Historical', 6],
                           ['First Speaker', 'Hari Seldon', 6],
                           ['Second Foundation', 'Kleise', 6],
                           ['Meirus', 'First', 6],
                           ['Fie', 'Anthor', 6],
                           ['Arcadia', 'Stettin', 6],
                           ['Arcadia', 'Palver', 6],
                           ['Darell', 'Lieutenant Dirige', 6],
                           ['Anthor', 'Turbor', 6],
                           ['Gaal Dornick', 'Supervisor', 5],
                           ['Gaal Dornick', 'Linge Chen', 5],
                           ['Pirenne', 'Dorwin', 5],
                           ['Empire', 'Dorwin', 5],
                           ['Board', 'Dorwin', 5],
                           ['Emperor', 'Dorwin', 5],
                           ['Second Foundation', 'Bort', 5],
                           ['Argo', 'Flober Mallow', 5],
                           ['Riose', 'Brodrig', 5],
                           ['Haven', 'Toran', 5],
                           ['Toran', 'Randu', 5],
                           ['Toran', 'Flan', 5],
                           ['Bayta', 'Empire', 5],
                           ['Twice Pritcher', 'Indbur', 5],
                           ['Haven', 'Mis', 5],
                           ['Commissioner', 'Mule', 5],
                           ['First', 'Fie', 5],
                           ['Anthor', 'Kleise', 5],
                           ['Callia', 'Mule', 5],
                           ['Meirus', 'Second Foundation', 5],
                           ['Arcadia', 'Fie', 5],
                           ['Anthor', 'Hari Seldon', 5],
                           ['Commissioner', 'Linge Chen', 4],
                           ['Emperor', 'Linge Chen', 4],
                           ['Hari Seldon', 'Linge Chen', 4],
                           ['Board', 'Chairman', 4],
                           ['Haut Rodric', 'Emperor', 4],
                           ['Senter', 'Second Foundation', 4],
                           ['Sermak', 'Hari Seldon', 4],
                           ['Sermak', 'Second Foundation', 4],
                           ['Sermak', 'Lewis', 4],
                           ['Lewis', 'Bort', 4],
                           ['Hardin', 'Bort', 4],
                           ['Ponyets', 'Gorm', 4],
                           ['Second Foundation', 'Twer', 4],
                           ['Flober Mallow', 'Empire', 4],
                           ['Hari Seldon', 'Twer', 4],
                           ['Korell', 'Empire', 4],
                           ['Barr', 'Bel', 4],
                           ['Korell', 'Riose', 4],
                           ['Brodrig', 'Cleon II', 4],
                           ['Emperor', 'Cleon II', 4],
                           ['Toran', 'Fie', 4],
                           ['Bayta', 'Randu', 4],
                           ['Hari Seldon', 'Flan', 4],
                           ['Randu', 'Hari Seldon', 4],
                           ['Empire', 'Seldon Historical', 4],
                           ['Haven', 'Flan', 4],
                           ['Indbur', 'Han', 4],
                           ['Ovall', 'Mule', 4],
                           ['First', 'Twice Pritcher', 4],
                           ['Fie', 'First Speaker', 4],
                           ['End', 'Hari Seldon', 4],
                           ['Channis', 'Han', 4],
                           ['Twice Pritcher', 'Elders', 4],
                           ['Channis', 'Elders', 4],
                           ['Darell', 'Hari Seldon', 4],
                           ['Toran', 'Darell', 4],
                           ['First', 'Seldon Historical', 4],
                           ['Second Foundation', 'Student', 4],
                           ['Homir', 'Turbor', 4],
                           ['Meirus', 'Callia', 4],
                           ['First', 'Poochie', 4],
                           ['Homir', 'Hari Seldon', 4],
                           ['First', 'Munn', 4],
                           ['Callia', 'Hari Seldon', 4],
                           ['First', 'Darell', 4],
                           ['Mamma', 'Second Foundation', 4],
                           ['Arcadia', 'Mamma', 4],
                           ['Arcadia', 'Lieutenant Dirige', 4],
                           ['Munn', 'Lieutenant Dirige', 4],
                           ['Munn', 'Callia', 4],
                           ['Darell', 'Palver', 4],
                           ['Gaal Dornick', 'Empire', 3],
                           ['Commissioner', 'Emperor', 3],
                           ['Avakim', 'Hari Seldon', 3],
                           ['Commissioner', 'Gaal Dornick', 3],
                           ['Advocate', 'Hari Seldon', 3],
                           ['Fie', 'Emperor', 3],
                           ['Lepold', 'Hari Seldon', 3],
                           ['Lepold', 'Empire', 3],
                           ['Walto', 'Bort', 3],
                           ['Sermak', 'Space', 3],
                           ['Aporat', 'Wienis', 3],
                           ['Gorov', 'Second Foundation', 3],
                           ['Privy Secretary', 'Second Foundation', 3],
                           ['Emperor', 'Flober Mallow', 3],
                           ['Korell', 'Hardin', 3],
                           ['Riose', 'Fie', 3],
                           ['Second Foundation', 'Bel', 3],
                           ['Barr', 'Lathan Devers', 3],
                           ['Fie', 'Flan', 3],
                           ['Bayta', 'Flan', 3],
                           ['Iwo', 'Flan', 3],
                           ['Ovall', 'Randu', 3],
                           ['Indbur', 'Randu', 3],
                           ['Indbur', 'Toran', 3],
                           ['Second Foundation', 'Han', 3],
                           ['Bayta', 'Dagobert IX', 3],
                           ['Commissioner', 'Magnifico', 3],
                           ['Mis', 'Fie', 3],
                           ['Twice Pritcher', 'Empire', 3],
                           ['End', 'Second Foundation', 3],
                           ['Student', 'Seldon Historical', 3],
                           ['Student', 'Hari Seldon', 3],
                           ['Homir', 'Semic', 3],
                           ['Turbor', 'Kleise', 3],
                           ['Semic', 'Second Foundation', 3],
                           ['Homir', 'First', 3],
                           ['Pappa', 'Second Foundation', 3],
                           ['Semic', 'Fie', 3],
                           ['Fie', 'Darell', 3],
                           ['Anthor', 'Lieutenant Dirige', 3],
                           ['Arcadia', 'First', 3],
                           ['Darell', 'Callia', 3],
                           ['Stettin', 'Darell', 3],
                           ['Palver', 'Turbor', 3],
                           ['Homir', 'Anthor', 3]]

    return connection_list


def get_candidates(ents_list, entity_list):
    candidates = []
    for ent in ents_list:
        candidates += [x[0] for x in entity_list for name in x if name == ent]
    candidates = list(set(candidates))
    return candidates
