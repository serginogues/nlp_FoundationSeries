from preprocess import *
from ner import named_entity_recognition
from cr import get_full_named_entities
from entity_connections import find_entity_links
from visualization import super_network

if __name__ == '__main__':

    if NER:
        if not parsed_list:
            parsed_list = preprocess(FoundationTrilogy)  # vector of preprocessed sentences

        people_list, location_list = named_entity_recognition(parsed_list)
        final_list = get_full_named_entities(people_list, parsed_list)  # chronological sequence of unified character occurrences
        # Up to here the code works perfect

    if LINKS:
        if not parsed_list:
            parsed_list = preprocess(FoundationTrilogy)  # vector of preprocessed sentences
        links_list = find_entity_links(final_list, parsed_list)

    super_network(links_list)

    #ToDo:
    # - co-reference handling (& pronoun handling and normalization of entities) before visualization.
    #   - resolve coreference cases like "Seldon" or "Foundation"
    # - measure the quality
    # - One or more visualizations. Word Cloud does not count as a visualization!
    #   - Custom Mapping: https://melaniewalsh.github.io/Intro-Cultural-Analytics/Mapping/Custom-Maps.html
    # - EXTRA bonus points
    #   - Detecting anomalies gets you bonus points
    #   - Creating a great video with audio also gets you bonus points
