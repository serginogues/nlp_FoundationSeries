"""
Given a text and a list of entities (post NER) find all connections between them
"""
from config import LINKS, combinations, tqdm
from cr import coreference_resolution


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


def solve_coreferences(candidates, token_list, entity_list, pos_current_token):
    """
    Solve coreferences
    :param candidates: list of entities
    :param token_list:
    :param entity_list:
    :param pos_current_token:
    :return:
    """
    if len(candidates) > 1:
        # check if token is surname
        name = token_list[pos_current_token - 1]
        entity2 = entity_from_token(entity_list, name)

        if len(entity2) == 1:
            entity = entity2[0]
        else:
            #TODO: Coreference resolution
            # Example: token = 'Seldon', get correct candidate from entity_list
            # https://towardsdatascience.com/how-to-make-an-effective-coreference-resolution-model-55875d2b5f19
            # https://neurosys.com/article/most-popular-frameworks-for-coreference-resolution/
            entity = coreference_resolution(candidates, token_list[pos_current_token - 100:pos_current_token + 100])
    else:
        entity = candidates[0]

    return entity


def entity_from_token(entity_list, token):
    return [x for x in entity_list for word in str(x[0]).split(" ") if str(token) == word]


def token_is_candidate(token):
    """
    :return: True if token is proper name or adjective
    """
    if token.pos_ == 'PROPN' or token.pos_ == 'ADJ':
        return True
    else:
        return False


def find_entity_links(entity_list, parsed_list):
    """
    For each entity
        For each sentence in text
            if entity is in sentence
    :return: a list of tuples
    """
    if LINKS:
        connection_list = []
        connection_list = family_links(entity_list, connection_list)

        token_list = [y for sent in parsed_list for y in sent]
        for i in tqdm(range(len(token_list))):

            token = token_list[i]
            if token_is_candidate(token):
                entity = entity_from_token(entity_list, token)

                if len(entity) > 0:

                    # Solve coreferences if more than one candidate
                    entity = solve_coreferences(entity, token_list, entity_list, i)

                    # find possible entities within the next 35 words
                    candidates = [x for x in token_list[i + 1:i + 35] if token_is_candidate(x)]
                    candidates = list(set(candidates))

                    # if any of the candidates corresponds to an entity, add connection
                    for cand in candidates:
                        entity2 = entity_from_token(entity_list, cand)
                        if len(entity2) > 0:
                            # Solve coreferences if more than one candidate
                            entity2 = solve_coreferences(entity2, token_list, entity_list, i)
                            connection_list = link_entities(connection_list, entity2, entity[0])

        connection_list = print_results_and_sort(entity_list, connection_list)
    else:
        connection_list = [['Second Empire', 'Second Foundation', 267], ['Second Foundation', 'The Mule', 188],
                           ['Second Foundation', 'Hari Seldon', 158], ['Second Foundation', 'Galactic Empire', 99],
                           ['Bayta Darell', 'Toran Darell', 90], ['Hari Seldon', 'Galactic Empire', 89],
                           ['Second Empire', 'The Mule', 87], ['Second Foundation', 'First Foundation', 86],
                           ['Arkady Darell', 'Pelleas Anthor', 82], ['Bayta Darell', 'Ebling Mis', 78],
                           ['Second Foundation', 'Ebling Mis', 77], ['Hari Seldon', 'Gaal Dornick', 70],
                           ['Magnifico Giganticus', 'Bayta Darell', 69], ['Bail Channis', 'The Mule', 68],
                           ['Second Empire', 'Hari Seldon', 66], ['Bayta Darell', 'The Mule', 65],
                           ['Toran Darell', 'Ebling Mis', 65], ['Bail Channis', 'Han Pritcher', 60],
                           ['Speaker', 'First Foundation', 57], ['Plan', 'Hari Seldon', 53],
                           ['Toran Darell', 'The Mule', 53], ['Ebling Mis', 'The Mule', 53],
                           ['Second Empire', 'First Foundation', 53], ['Second Foundation', 'Bail Channis', 53],
                           ['Galactic Empire', 'Second Empire', 51], ['The Mule', 'Han Pritcher', 49],
                           ['Magnifico Giganticus', 'The Mule', 47], ['Second Empire', 'Bail Channis', 47],
                           ['Arkady Darell', 'Arcadia Darell', 47], ['Jorane Sutt', 'Hober Mallow', 46],
                           ['Homir Munn', 'Second Foundation', 46], ['Magnifico Giganticus', 'Toran Darell', 45],
                           ['Hober Mallow', 'Second Foundation', 44], ['Magnifico Giganticus', 'Ebling Mis', 44],
                           ['The Mule', 'First Foundation', 44], ['Han Pritcher', 'Second Foundation', 42],
                           ['Hari Seldon', 'The Mule', 41], ['Ankor Jael', 'Hober Mallow', 40],
                           ['Second Empire', 'Ebling Mis', 40], ['Homir Munn', 'Arcadia Darell', 40],
                           ['Pelleas Anthor', 'Homir Munn', 39], ['First Foundation', 'Hari Seldon', 37],
                           ['Galactic Empire', 'The Mule', 37], ['Seldon Hardin', 'Salvor Hardin', 36],
                           ['Ducem Barr', 'Bel Riose', 36], ['Arkady Darell', 'Homir Munn', 36],
                           ['Seldon Hardin', 'Hari Seldon', 35], ['Second Foundation', 'Bayta Darell', 35],
                           ['Second Foundation', 'Plan', 34], ['Lewis Pirenne', 'Seldon Hardin', 33],
                           ['Toran Darell', 'Second Foundation', 33], ['Seldon Hardin', 'Wienis', 32],
                           ['Ebling Mis', 'Hari Seldon', 32], ['Galactic Empire', 'First Foundation', 31],
                           ['Han Pritcher', 'Ebling Mis', 31], ['Second Foundation', 'Seldon Hardin', 30],
                           ['Commdor Asper', 'Hober Mallow', 30], ['Second Foundation', 'Pelleas Anthor', 30],
                           ['Seldon Hardin', 'Yohan Lee', 29], ['Indbur', 'Ebling Mis', 27],
                           ['Arkady Darell', 'Second Foundation', 27], ['Seldon Hardin', 'Sef Sermak', 26],
                           ['Randu', 'The Mule', 26], ['Second Foundation', 'Fie', 26], ['Fie', 'The Mule', 25],
                           ['Plan', 'Second Empire', 24], ['Elvett Semic', 'Pelleas Anthor', 24],
                           ['Stettin', 'Homir Munn', 24], ['Hari Seldon', 'Emperor', 23],
                           ['Hober Mallow', 'Hari Seldon', 23], ['Ducem Barr', 'Second Foundation', 23],
                           ['Arkady Darell', 'Second Empire', 23], ['Jole Turbor', 'Arkady Darell', 23],
                           ['Second Empire', 'Pelleas Anthor', 23], ['Bel Riose', 'Galactic Empire', 22],
                           ['Bail Channis', 'First Foundation', 22], ['Homir Munn', 'Second Empire', 22],
                           ['Pappa', 'Arcadia Darell', 22], ['Second Foundationer', 'Second Empire', 21],
                           ['The Mule', 'Homir Munn', 21], ['Mamma', 'Pappa', 21], ['Fie', 'Hari Seldon', 20],
                           ['Second Foundation', 'Randu', 20], ['Han Pritcher', 'Flan Pritcher', 20],
                           ['Second Empire', 'Han Pritcher', 20], ['Plan', 'First Foundation', 20],
                           ['Second Foundation', 'Arcadia Darell', 20], ['Seldon Hardin', 'Verisof', 19],
                           ['Jole Turbor', 'Pelleas Anthor', 19], ['Kleise', 'Arkady Darell', 19],
                           ['Jole Turbor', 'Second Foundation', 19], ['Lathan Devers', 'Ducem Barr', 18],
                           ['Han Pritcher', 'Toran Darell', 18], ['Student', 'Speaker', 18],
                           ['Stettin', 'Second Foundation', 18], ['Emperor', 'Galactic Empire', 17],
                           ['Lepold', 'Wienis', 17], ['Galactic Empire', 'Ducem Barr', 17],
                           ['Salvor Hardin', 'Hober Mallow', 17], ['Flan Pritcher', 'The Mule', 17],
                           ['Student', 'First Foundation', 17], ['Arkady Darell', 'Elvett Semic', 17],
                           ['Ducem Barr', 'Emperor', 16], ['Second Foundation', 'Indbur', 16],
                           ['Ovall Gri', 'Randu', 16],
                           ['Fie', 'Second Empire', 16], ['Speaker', 'Second Empire', 16],
                           ['Hari Seldon', 'Jord Fara', 15],
                           ['Jord Fara', 'Seldon Hardin', 15], ['Ducem Barr', 'Hober Mallow', 15],
                           ['Bel Riose', 'Second Foundation', 15], ['Emperor', 'Brodrig', 15],
                           ['Han Pritcher', 'Bayta Darell', 15], ['Randu', 'Ebling Mis', 15], ['The Mule', 'Plan', 15],
                           ['Plan', 'Speaker', 15], ['Homir Munn', 'Jole Turbor', 15],
                           ['Jole Turbor', 'Second Empire', 15],
                           ['Hari Seldon', 'Homir Munn', 15], ['Mamma', 'Arcadia Darell', 15],
                           ['Master', 'Hober Mallow', 14], ['Bel Riose', 'Emperor', 14], ['Randu', 'Hari Seldon', 14],
                           ['Hari Seldon', 'Bayta Darell', 14], ['The Mule', 'Speaker', 14],
                           ['Speaker', 'Second Foundation', 14], ['Pelleas Anthor', 'Arcadia Darell', 14],
                           ['Pelleas Anthor', 'Hari Seldon', 14], ['Arcadia Darell', 'The Mule', 14],
                           ['Salvor Hardin', 'Hari Seldon', 13], ['Yohan Lee', 'Hari Seldon', 13],
                           ['Second Foundation', 'Lepold', 13], ['Bel Riose', 'Hari Seldon', 13],
                           ['Ducem Barr', 'Hari Seldon', 13], ['Second Foundation', 'Fran', 13],
                           ['Indbur', 'Mayor Hardin', 13], ['Hari Seldon', 'Raven Seldon', 12],
                           ['Emperor', 'Seldon Hardin', 12], ['Dorwin', 'Seldon Hardin', 12],
                           ['Salvor Hardin', 'Second Foundation', 12], ['Eskel Gorov', 'Limmar Ponyets', 12],
                           ['Ankor Jael', 'Jorane Sutt', 12], ['Plan', 'Galactic Empire', 12],
                           ['Magnifico Giganticus', 'Second Foundation', 12], ['Speaker', 'Hari Seldon', 12],
                           ['Homir Munn', 'Flomir Munn', 12], ['Sef Sermak', 'Yohan Lee', 11],
                           ['Wienis', 'Second Foundation', 11], ['Lewis Bort', 'Sef Sermak', 11],
                           ['Jorane Sutt', 'Hari Seldon', 11], ['Commdor Asper', 'Second Foundation', 11],
                           ['Second Foundation', 'Lathan Devers', 11], ['Brodrig', 'Ducem Barr', 11],
                           ['Randu', 'Toran Darell', 11], ['Indbur', 'Hari Seldon', 11], ['Bail Channis', 'Fie', 11],
                           ['Speaker', 'Bail Channis', 11], ['Second Empire', 'Arcadia Darell', 11],
                           ['First Foundation', 'Stettin', 11], ['Hari Seldon', 'Linge Chen', 10],
                           ['Seldon Hardin', 'Mayor Hardin', 10], ['Seldon Hardin', 'Lepold', 10],
                           ['Ducem Barr', 'Onum Barr', 10], ['Hober Mallow', 'Sennett Forell', 10],
                           ['Randu', 'Fran', 10],
                           ['Han Pritcher', 'Fie', 10], ['Indbur', 'The Mule', 10], ['Homir Munn', 'Elvett Semic', 10],
                           ['Second Empire', 'Kleise', 10], ['Stettin', 'The Mule', 10], ['Arkady Darell', 'Fie', 10],
                           ['Fie', 'Pelleas Anthor', 10], ['Lewis Pirenne', 'Emperor', 9],
                           ['Seldon Hardin', 'Jorane Sutt', 9], ['Emperor', 'Second Foundation', 9],
                           ['Theo Aporat', 'Wienis', 9], ['Master', 'Limmar Ponyets', 9], ['Eskel Gorov', 'Master', 9],
                           ['Second Foundation', 'Master', 9], ['Hober Mallow', 'Seldon Hardin', 9],
                           ['Ducem Barr', 'Sennett Forell', 9], ['Second Foundation', 'Flan Pritcher', 9],
                           ['Second Foundation', 'Jord Commason', 9], ['First Foundation', 'Ebling Mis', 9],
                           ['Bayta Darell', 'Arkady Darell', 9], ['Kleise', 'Pelleas Anthor', 9],
                           ['Second Foundation', 'Kleise', 9], ['Lev Meirus', 'Second Foundation', 9],
                           ['Stettin', 'Arcadia Darell', 9], ['Gaal Dornick', 'Fiari Seldon', 8],
                           ['Gaal Dornick', 'Linge Chen', 8], ['Galactic Empire', 'Seldon Hardin', 8],
                           ['Yohan Lee', 'Salvor Hardin', 8], ['Master', 'Pherl', 8], ['Bel Riose', 'Brodrig', 8],
                           ['Hari Seldon', 'Toran Darell', 8], ['Han Pritcher', 'Indbur', 8],
                           ['Flan Pritcher', 'Fie', 8],
                           ['Jord Commason', 'The Mule', 8], ['Second Empire', 'Toran Darell', 8],
                           ['Bail Channis', 'Second Foundationer', 8], ['Bail Channis', 'Ebling Mis', 8],
                           ['The Mule', 'Arkady Darell', 8], ['Student', 'Plan', 8], ['Elvett Semic', 'Jole Turbor', 8],
                           ['Elvett Semic', 'Second Empire', 8], ['Elvett Semic', 'Second Foundation', 8],
                           ['Mayor Hardin', 'Second Foundation', 7], ['Hari Seldon', 'Sef Sermak', 7],
                           ['Verisof', 'Galactic Empire', 7], ['Salvor Hardin', 'Wienis', 7],
                           ['Lewis Bort', 'Seldon Hardin', 7], ['Jorane Sutt', 'Second Foundation', 7],
                           ['Fran', 'Toran Darell', 7], ['Fie', 'Toran Darell', 7],
                           ['Ovall Gri', 'Second Foundation', 7],
                           ['Randu', 'Indbur', 7], ['Ovall Gri', 'The Mule', 7], ['Ebling Mis', 'Fie', 7],
                           ['Second Empire', 'Bayta Darell', 7], ['Fie', 'First Foundation', 7], ['Fie', 'Plan', 7],
                           ['Elvett Semic', 'Arcadia Darell', 7], ['First Foundation', 'Homir Munn', 7],
                           ['Arcadia Darell', 'Fie', 7], ['Preem Palver', 'Arcadia Darell', 7],
                           ['Gaal Dornick', 'Galactic Empire', 6], ['Second Foundation', 'Jord Fara', 6],
                           ['Mayor Hardin', 'Jord Fara', 6], ['Second Foundation', 'Sef Sermak', 6],
                           ['Salvor Hardin', 'Lepold', 6], ['Lepold', 'Verisof', 6],
                           ['Galactic Empire', 'Hober Mallow', 6],
                           ['Ducem Barr', 'Fie', 6], ['Bayta Darell', 'Galactic Empire', 6], ['Dad', 'Toran Darell', 6],
                           ['Magnifico Giganticus', 'Han Pritcher', 6], ['Lee Senter', 'Yohan Lee', 6],
                           ['Fie', 'Speaker', 6], ['Hari Seldon', 'Arcadia Darell', 6],
                           ['Arkady Darell', 'Hari Seldon', 6],
                           ['Fie', 'Homir Munn', 6], ['Lev Meirus', 'First Foundation', 6], ['Fie', 'Flomir Munn', 6],
                           ['Gaal Dornick', 'Raven Seldon', 5], ['Avakim', 'Gaal Dornick', 5],
                           ['Emperor', 'Linge Chen', 5],
                           ['Lewis Pirenne', 'Salvor Hardin', 5], ['Second Foundation', 'Lewis Pirenne', 5],
                           ['Yohan Lee', 'Second Foundation', 5], ['Seldon Hardin', 'The Mule', 5],
                           ['Wienis', 'Verisof', 5],
                           ['Galactic Empire', 'Lepold', 5], ['Second Foundation', 'Lewis Bort', 5],
                           ['Eskel Gorov', 'Galactic Empire', 5], ['Sennett Forell', 'Galactic Empire', 5],
                           ['Bel Riose', 'Sennett Forell', 5], ['Bayta Darell', 'Randu', 5], ['Han Pritcher', 'Fox', 5],
                           ['Fox', 'The Mule', 5], ['Bayta Darell', 'Jord Commason', 5],
                           ['Jord Commason', 'Magnifico Giganticus', 5], ['Second Foundationer', 'The Mule', 5],
                           ['Plan', 'Arcadia Darell', 5], ['Stettin', 'Second Empire', 5],
                           ['First Foundation', 'Arkady Darell', 5], ['Second Foundation', 'Pappa', 5],
                           ['Mamma', 'Homir Munn', 5], ['Preem Palver', 'Pappa', 5], ['Gaal Dornick', 'Emperor', 4],
                           ['Hari Seldon', 'Advocate', 4], ['Lewis Pirenne', 'Jord Fara', 4],
                           ['Seldon Hardin', 'Fulham', 4],
                           ['Dorwin', 'Mayor Hardin', 4], ['Yohan Lee', 'Verisof', 4],
                           ['Second Foundation', 'dryly', 4],
                           ['Verisof', 'Hari Seldon', 4], ['Hari Seldon', 'Lepold', 4], ['Salvor Hardin', 'Verisof', 4],
                           ['Walto', 'Sef Sermak', 4], ['Lewis Bort', 'Walto', 4], ['Eskel Gorov', 'Les Gorm', 4],
                           ['Second Foundation', 'Eskel Gorov', 4], ['Master', 'Jorane Sutt', 4],
                           ['Hober Mallow', 'Fie', 4],
                           ['Jord Fara', 'Hober Mallow', 4], ['Hober Mallow', 'Emperor', 4],
                           ['Jorane Sutt', 'Commdor Asper', 4], ['Ankor Jael', 'Hari Seldon', 4],
                           ['Hari Seldon', 'Sennett Forell', 4], ['Bel Riose', 'First Foundation', 4],
                           ['Fie', 'Emperor', 4],
                           ['Brodrig', 'Second Foundation', 4], ['Lathan Devers', 'Galactic Empire', 4],
                           ['Fran', 'Bayta Darell', 4], ['Fran', 'Hari Seldon', 4], ['Iwo', 'Fran', 4],
                           ['Jord Commason', 'Jord Fara', 4], ['Jord Commason', 'Toran Darell', 4],
                           ['Bail Channis', 'Elders', 4], ['Pelleas Anthor', 'Toran Darell', 4],
                           ['Student', 'Hari Seldon', 4], ['Second Empire', 'Student', 4], ['Kleise', 'Jole Turbor', 4],
                           ['Homir Munn', 'Kleise', 4], ['The Mule', 'Pelleas Anthor', 4], ['Lev Meirus', 'Stettin', 4],
                           ['Poochie', 'Second Foundation', 4], ['Plan', 'Homir Munn', 4],
                           ['Poochie', 'Arcadia Darell', 4],
                           ['Second Foundation', 'Mamma', 4], ['Fie', 'Elvett Semic', 4],
                           ['Pelleas Anthor', 'Hober Mallow', 4], ['Preem Palver', 'Second Foundation', 4],
                           ['Arkady Darell', 'Preem Palver', 4], ['Jole Turbor', 'Preem Palver', 4],
                           ['Flomir Munn', 'Pelleas Anthor', 4], ['The Mule', 'Jole Turbor', 4],
                           ['Hari Seldon', 'Fiari Seldon', 3], ['Emperor', 'Avakim', 3], ['Fulham', 'Jord Fara', 3],
                           ['Galactic Empire', 'Dorwin', 3], ['Mayor Hardin', 'Jorane Sutt', 3],
                           ['Mayor Hardin', 'Fulham', 3], ['Jorane Sutt', 'Galactic Empire', 3],
                           ['Mayor Hardin', 'Hari Seldon', 3], ['Second Foundation', 'Verisof', 3],
                           ['Wienis', 'Galactic Empire', 3], ['Lewis Pirenne', 'Sef Sermak', 3],
                           ['Salvor Hardin', 'Mayor Hardin', 3], ['Fie', 'Theo Aporat', 3],
                           ['Second Foundation', 'Les Gorm', 3], ['Second Foundation', 'Limmar Ponyets', 3],
                           ['Eskel Gorov', 'Pherl', 3], ['Onum Barr', 'Hober Mallow', 3],
                           ['Galactic Empire', 'Onum Barr', 3], ['Salvor Hardin', 'Ankor Jael', 3],
                           ['Salvor Hardin', 'The Mule', 3], ['Second Foundation', 'Sennett Forell', 3],
                           ['Salvor Hardin', 'Sennett Forell', 3], ['Second Empire', 'Sennett Forell', 3],
                           ['Fie', 'Galactic Empire', 3], ['Brodrig', 'Galactic Empire', 3],
                           ['Brodrig', 'Lathan Devers', 3],
                           ['Lathan Devers', 'Emperor', 3], ['Fie', 'Bayta Darell', 3], ['dryly', 'Hari Seldon', 3],
                           ['The Mule', 'Fran', 3], ['Indbur', 'Bayta Darell', 3], ['Jord Commason', 'Ebling Mis', 3],
                           ['First Foundation', 'Flan Pritcher', 3], ['Hari Seldon', 'Han Pritcher', 3],
                           ['Elders', 'Han Pritcher', 3], ['Second Foundation', 'Second Foundationer', 3],
                           ['Han Pritcher', 'Second Foundationer', 3], ['Arkady Darell', 'Plan', 3],
                           ['Hober Mallow', 'The Mule', 3], ['Toran Darell', 'Arkady Darell', 3],
                           ['Student', 'Second Foundation', 3], ['Poochie', 'The Mule', 3], ['Stettin', 'Poochie', 3],
                           ['Arcadia Darell', 'First Foundation', 3], ['Galactic Empire', 'Homir Munn', 3],
                           ['Arkady Darell', 'Hober Mallow', 3], ['Arkady Darell', 'Stettin', 3],
                           ['Arkady Darell', 'Flomir Munn', 3], ['Hari Seldon', 'Avakim', 2],
                           ['Advocate', 'Galactic Empire', 2], ['Gaal Dornick', 'Fie', 2], ['Salvor Hardin', 'Fie', 2],
                           ['Seldon Hardin', 'Fie', 2], ['Jord Fara', 'Jorane Sutt', 2], ['Jorane Sutt', 'Dorwin', 2],
                           ['Emperor', 'Mayor Hardin', 2], ['Hari Seldon', 'Fulham', 2], ['Emperor', 'Dorwin', 2],
                           ['Sef Sermak', 'Mayor Hardin', 2], ['Mayor Hardin', 'Verisof', 2], ['Verisof', 'Plan', 2],
                           ['Salvor Hardin', 'Galactic Empire', 2], ['Lewis Bort', 'Lewis Pirenne', 2],
                           ['Sef Sermak', 'Salvor Hardin', 2], ['Galactic Empire', 'Lewis Bort', 2],
                           ['Emperor', 'Lepold', 2], ['Wienis', 'Hari Seldon', 2], ['Mayor Hardin', 'Wienis', 2],
                           ['Lewis Pirenne', 'Hari Seldon', 2], ['Lewis Bort', 'Hari Seldon', 2],
                           ['Les Gorm', 'Limmar Ponyets', 2], ['Fie', 'Master', 2], ['Elders', 'Pherl', 2],
                           ['Jord Fara', 'Galactic Empire', 2], ['Capsule', 'Second Foundation', 2],
                           ['Galactic Empire', 'Commdor Asper', 2], ['Ankor Jael', 'Seldon Hardin', 2],
                           ['Second Foundation', 'Ankor Jael', 2], ['Fie', 'Sennett Forell', 2],
                           ['dryly', 'Sennett Forell', 2], ['Fie', 'Bel Riose', 2], ['dryly', 'Brodrig', 2],
                           ['Lathan Devers', 'Bel Riose', 2], ['Brodrig', 'Hari Seldon', 2],
                           ['Sennett Forell', 'Lathan Devers', 2], ['Bayta Darell', 'Dad', 2], ['Fie', 'Fran', 2],
                           ['Second Foundationer', 'Fran', 2], ['Dad', 'Fie', 2], ['Randu', 'Lathan Devers', 2],
                           ['Fran', 'Lathan Devers', 2], ['Plan', 'Bel Riose', 2], ['Han Pritcher', 'Fran', 2],
                           ['Han Pritcher', 'Mayor Hardin', 2], ['Indbur', 'Flan Pritcher', 2],
                           ['Mayor Hardin', 'Flan Pritcher', 2], ['Fie', 'Mayor Hardin', 2], ['Fie', 'Indbur', 2],
                           ['Capsule', 'Flan Pritcher', 2], ['Iwo', 'The Mule', 2], ['Ovall Gri', 'Fie', 2],
                           ['dryly', 'Ovall Gri', 2], ['Mayor Hardin', 'Ebling Mis', 2],
                           ['Magnifico Giganticus', 'Randu', 2], ['Indbur', 'Magnifico Giganticus', 2],
                           ['Indbur', 'Toran Darell', 2], ['Fie', 'Fox', 2], ['Capsule', 'Jord Commason', 2],
                           ['Toran Darell', 'First Foundation', 2], ['Ebling Mis', 'Galactic Empire', 2],
                           ['Han Pritcher', 'Galactic Empire', 2], ['Bail Channis', 'Galactic Empire', 2],
                           ['First Foundation', 'Han Pritcher', 2], ['Elders', 'Second Empire', 2],
                           ['Elders', 'Second Foundation', 2], ['Hari Seldon', 'Bail Channis', 2],
                           ['Ebling Mis', 'Speaker', 2], ['Bayta Darell', 'Arcadia Darell', 2],
                           ['Plan', 'Salvor Hardin', 2],
                           ['Plan', 'Hober Mallow', 2], ['The Mule', 'Student', 2], ['Fie', 'Student', 2],
                           ['Elvett Semic', 'Kleise', 2], ['Elvett Semic', 'The Mule', 2],
                           ['First Foundation', 'Poochie', 2], ['Lev Meirus', 'Poochie', 2],
                           ['Lev Meirus', 'The Mule', 2],
                           ['Lev Meirus', 'Second Empire', 2], ['Homir Munn', 'Poochie', 2],
                           ['Second Foundationer', 'Arkady Darell', 2], ['Stettin', 'Flomir Munn', 2],
                           ['Homir Munn', 'Bayta Darell', 2], ['Pappa', 'Homir Munn', 2], ['Pappa', 'Stettin', 2],
                           ['Mamma', 'Preem Palver', 2], ['Arkady Darell', 'Galactic Empire', 2],
                           ['Galactic Empire', 'Stettin', 2], ['Preem Palver', 'Second Empire', 2],
                           ['Mamma', 'The Mule', 2],
                           ['Jole Turbor', 'Stettin', 2], ['Jole Turbor', 'Hari Seldon', 2],
                           ['Arcadia Darell', 'Jole Turbor', 2], ['Preem Palver', 'The Mule', 2],
                           ['Homir Munn', 'Lev Meirus', 2], ['Arkady Darell', 'Lev Meirus', 2],
                           ['Arkady Darell', 'Speaker', 2], ['Speaker', 'Preem Palver', 2],
                           ['First Foundation', 'Preem Palver', 2], [['Arkady Darell'], ['Bayta Darell'], 1],
                           [['Arkady Darell'], ['Toran Darell'], 1], [['Arkady Darell'], ['Arcadia Darell'], 1],
                           [['Hari Seldon'], ['Raven Seldon'], 1], [['Hari Seldon'], ['Fiari Seldon'], 1],
                           [['Raven Seldon'], ['Fiari Seldon'], 1], [['Seldon Hardin'], ['Salvor Hardin'], 1],
                           [['Seldon Hardin'], ['Mayor Hardin'], 1], [['Ducem Barr'], ['Onum Barr'], 1],
                           [['Bayta Darell'], ['Toran Darell'], 1], [['Bayta Darell'], ['Arcadia Darell'], 1],
                           [['Salvor Hardin'], ['Mayor Hardin'], 1], [['Toran Darell'], ['Arcadia Darell'], 1],
                           [['Homir Munn'], ['Flomir Munn'], 1], [['Han Pritcher'], ['Flan Pritcher'], 1],
                           [['Galactic Empire'], ['Second Empire'], 1],
                           [['Second Foundation'], ['First Foundation'], 1],
                           ['First Foundation', 'Gaal Dornick', 1], ['Fiari Seldon', 'Emperor', 1],
                           ['Fie', 'Lewis Pirenne', 1], ['Mayor Hardin', 'Lewis Pirenne', 1],
                           ['dryly', 'Seldon Hardin', 1],
                           ['Fulham', 'Jorane Sutt', 1], ['Lewis Pirenne', 'Jorane Sutt', 1],
                           ['Lewis Pirenne', 'Fulham', 1],
                           ['Dorwin', 'Hari Seldon', 1], ['Lameth', 'Seldon Hardin', 1],
                           ['Mayor Hardin', 'Galactic Empire', 1], ['Dorwin', 'Lewis Pirenne', 1],
                           ['Jord Fara', 'Yohan Lee', 1], ['Yohan Lee', 'Fie', 1], ['Yohan Lee', 'The Mule', 1],
                           ['dryly', 'Verisof', 1], ['Wienis', 'dryly', 1], ['Plan', 'Seldon Hardin', 1],
                           ['Lepold', 'The Mule', 1], ['Salvor Hardin', 'Lewis Bort', 1], ['Seldon Hardin', 'Walto', 1],
                           ['Lewis Bort', 'Verisof', 1], ['Wienis', 'Sef Sermak', 1], ['Walto', 'Lepold', 1],
                           ['Emperor', 'Wienis', 1], ['Theo Aporat', 'Galactic Empire', 1],
                           ['Galactic Empire', 'Limmar Ponyets', 1], ['Seldon Hardin', 'Limmar Ponyets', 1],
                           ['Salvor Hardin', 'Limmar Ponyets', 1], ['Salvor Hardin', 'Jorane Sutt', 1],
                           ['Jord Fara', 'Master', 1], ['Emperor', 'Second Empire', 1], ['Master', 'Commdor Asper', 1],
                           ['Fie', 'Jord Fara', 1], ['Ankor Jael', 'Fie', 1], ['Ankor Jael', 'Commdor Asper', 1],
                           ['Hober Mallow', 'Bel Riose', 1], ['Seldon Hardin', 'Bel Riose', 1],
                           ['First Foundation', 'Emperor', 1], ['dryly', 'Fie', 1], ['dryly', 'Bel Riose', 1],
                           ['Ducem Barr', 'dryly', 1], ['Bel Riose', 'The Mule', 1], ['Emperor', 'The Mule', 1],
                           ['Second Empire', 'Ducem Barr', 1], ['The Mule', 'Sennett Forell', 1], ['Randu', 'Dad', 1],
                           ['Fran', 'Dad', 1], ['Second Foundationer', 'Toran Darell', 1],
                           ['Fie', 'Second Foundationer', 1],
                           ['Galactic Empire', 'Randu', 1], ['Second Foundation', 'Dad', 1], ['Capsule', 'Fie', 1],
                           ['dryly', 'Toran Darell', 1], ['Bayta Darell', 'dryly', 1],
                           ['Toran Darell', 'Seldon Hardin', 1],
                           ['Bayta Darell', 'Seldon Hardin', 1], ['dryly', 'Ebling Mis', 1],
                           ['Iwo', 'Second Foundation', 1],
                           ['Fie', 'Randu', 1], ['The Mule', 'dryly', 1], ['Randu', 'Capsule', 1],
                           ['Mayor Hardin', 'Bayta Darell', 1], ['Indbur', 'Hober Mallow', 1], ['The Mule', 'Hella', 1],
                           ['Indbur', 'Fox', 1], ['Toran Darell', 'Galactic Empire', 1],
                           ['Jord Commason', 'Galactic Empire', 1], ['The Mule', 'Capsule', 1],
                           ['Magnifico Giganticus', 'Yohan Lee', 1], ['Magnifico Giganticus', 'Lee Senter', 1],
                           ['Magnifico Giganticus', 'Hari Seldon', 1], ['Flan Pritcher', 'Bail Channis', 1],
                           ['Elders', 'The Mule', 1], ['Galactic Empire', 'Elders', 1], ['Bail Channis', 'Plan', 1],
                           ['Pelleas Anthor', 'Plan', 1], ['Speaker', 'Galactic Empire', 1],
                           ['Student', 'Galactic Empire', 1], ['The Mule', 'Kleise', 1],
                           ['Galactic Empire', 'Pelleas Anthor', 1], ['Lathan Devers', 'Hari Seldon', 1],
                           ['Lathan Devers', 'Seldon Hardin', 1], ['Lathan Devers', 'Hober Mallow', 1],
                           ['The Mule', 'Lathan Devers', 1], ['Lev Meirus', 'Galactic Empire', 1],
                           ['Arcadia Darell', 'Galactic Empire', 1], ['Poochie', 'Galactic Empire', 1],
                           ['Second Foundationer', 'Kleise', 1], ['Fie', 'Kleise', 1], ['The Mule', 'Flomir Munn', 1],
                           ['Stettin', 'Fie', 1], ['Fie', 'Mamma', 1], ['Fie', 'Pappa', 1], ['Stettin', 'Mamma', 1],
                           ['First Foundation', 'Pappa', 1], ['Pappa', 'The Mule', 1], ['Jole Turbor', 'Plan', 1],
                           ['Flomir Munn', 'Hari Seldon', 1], ['Arcadia Darell', 'Second Foundationer', 1],
                           ['Pelleas Anthor', 'Second Foundationer', 1], ['Arcadia Darell', 'Student', 1],
                           ['Arkady Darell', 'Student', 1], ['Arcadia Darell', 'Speaker', 1]]

    return connection_list


def print_results_and_sort(entity_list, connection_list):
    for i, name in enumerate(entity_list):
        conn = [x for x in connection_list if name[0] in x]
        print(i, "-", name[0], len(conn), "list: ", conn)

    def takethird(elem):
        return elem[2]

    connection_list.sort(key=takethird, reverse=True)

    return connection_list
