from config import FoundationTrilogy, VISUALIZE
from preprocess import preprocess
from ner import named_entity_recognition
from ne_complete_names import get_full_named_entities
from entity_connections import find_entity_links
from visualization import super_network

"""
*********PIPELINE*********
0 - preprocess.py           - preprocess()
1 - ner.py                  - named_entity_recognition()
2 - ne_complete_names.py    - get_full_named_entities()
3 - CR + ALIAS RESOLUTION
4 - CR + ENTITY RELATIONS
5 - NORMALIZATION
6 - VISUALIZATION
7 - QUALITY VALIDATION
"""

if __name__ == '__main__':

    parsed_list = preprocess(FoundationTrilogy)  # vector of preprocessed sentences

    people_list, location_list = named_entity_recognition(parsed_list)

    final_list = get_full_named_entities(people_list, parsed_list)  # Final List of characters

    # Up to here the code works perfect
    #TODO:
    # - Alias resolution - pattern: PERSON + ["known as" OR ", "
    # - Entity Relations (ideas in course 5 diapo 34)
    # - Coreferences for entity connection
    # - Use normalization of extracted entities before visualization
    # - Visualization: Custom Mapping with https://melaniewalsh.github.io/Intro-Cultural-Analytics/Mapping/Custom-Maps.html
    # - Measure Quality:
    #   - Do a random validation of quality, avoid to blindly apply libraries without understanding
    #   how they work or what the quality is. So, the need to measure that by a small (50-100) random manual validations.
    #   - Also incorporate multi-juror validation and calculate a kappa distance in the above

    links_list = find_entity_links(final_list, parsed_list)

    if VISUALIZE:
        super_network(links_list)

    # ToDo: EXTRA bonus points
    #   - Detecting anomalies gets you bonus points
    #   - Creating a great video with audio also gets you bonus points
