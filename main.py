from config import FoundationTrilogy
from preprocess import preprocess
from ner import named_entity_recognition
from entity_connections import entity_links
from normalization import normalize_list
from visualization import super_network

"""
*********PIPELINE*********
0 - preprocess.py           - preprocess()                  - DONE
1 - ner.py                  - NER + normalization           - DONE
2 - CR + ALIAS RESOLUTION
4 - CR + ENTITY RELATIONS
5 - NORMALIZATION
6 - VISUALIZATION
7 - QUALITY VALIDATION
"""

if __name__ == '__main__':

    # text = FoundationTrilogy[:-1200000]
    text = FoundationTrilogy
    parsed_list = preprocess(text, True)  # vector of preprocessed sentences
    people_list, location_list, unclassified = named_entity_recognition(parsed_list, False)
    people_list = normalize_list(people_list, unclassified, False)
    people_links, location_links = entity_links(people_list, location_list, parsed_list, True)
    super_network(people_links, False)

    #TODO:
    # - CR
    # - Visualization:
    #   - Custom Mapping with
    #   - Events: see course 5 slide 47 (tree graph)
    # - Validation

    # TODO: EXTRA bonus points
    #   - Detecting anomalies gets you bonus points
    #   - Creating a great video with audio also gets you bonus points
