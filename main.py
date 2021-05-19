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

    text = FoundationTrilogy

    parsed_list = preprocess(text, False)  # vector of preprocessed sentences

    people_list, location_list, unclassified = named_entity_recognition(parsed_list, False)

    people_list = normalize_list(people_list, unclassified, True)

    # Up to here the code works perfect
    #TODO:
    # - Coreferences for entity connection
    # - Visualization:
    #   - Custom Mapping with https://melaniewalsh.github.io/Intro-Cultural-Analytics/Mapping/Custom-Maps.html
    #   - Events: see course 5 slide 47 (tree graph)
    # - Measure Quality:
    #   - Do a random validation of quality, avoid to blindly apply libraries without understanding
    #   how they work or what the quality is. So, the need to measure that by a small (50-100) random manual validations.
    #   - Also incorporate multi-juror validation and calculate a kappa distance in the above

    links_list = entity_links(people_list, parsed_list)

    super_network(links_list)

    # TODO: EXTRA bonus points
    #   - Detecting anomalies gets you bonus points
    #   - Creating a great video with audio also gets you bonus points
