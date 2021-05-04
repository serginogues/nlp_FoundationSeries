from preprocess import *
from ner import entity_identification
from correference_resolution import coreference_resolution
from entity_connections import entity_relationship
from visualization import super_network

"""
https://arxiv.org/pdf/1907.02704.pdf
1) The identification of characters. We distinguish two substeps:
    - Detect occurrences of characters in the narrative
        -  a character can appear under three forms in text: proper noun, nominal, and pronoun.
    - Unify these occurrences, i.e. to determine which ones correspond to the same character. 
    In a text, the same character can appear under different names. 
    As mentioned before, characters occurrences appear under three forms in text: proper nouns, nominals, and pronouns. 
    Unifying these occurrences can be considered as a specific version of the coreference resolution problem, 
    which consists in identifying sequences of expressions, called coreference chains, that represent the same concept.
    - The output of this step takes the form of a chronological sequence of unified character occurrences.

2) Detecting interactions between characters.
    - take into account conversations, and to consider that two characters interact when one talks to the other.
    With certain forms of narrative such as plays, in which speakers are given, this task is relatively straightforward.
    - situations where one character talks about the other.
    - all sorts of actions one character can perform on the other (besides conversing).
    - explicit or inferred social relationships such as being married, being relatives, or working together
    The output of the second step is a chronological sequence of interactions between characters.

3) The extraction of the proper graph
    - preprocess: simplifying the sequence of interactions by filtering and/or merging some of the characters under certain conditions.
    For example, when considering co-occurrences, some authors merge characters that always appear together
    - temporal integration, i.e. the aggregation of the previously identified interactions.
        - full integration and therefore leading to a static network, and those performing only
        a partial integration, and producing a dynamic network.
"""


if __name__ == '__main__':

    parsed_list = preprocess(FoundationTrilogy)
    people_list, location_list = entity_identification(parsed_list)
    final_list = coreference_resolution(people_list, parsed_list)  # chronological sequence of unified character occurrences
    print("CR and entity extraction finished. Found:", len(final_list), "characters.")
    links_list = entity_relationship(final_list, FoundationTrilogy)
    super_network(links_list)

    #ToDo:
    # - co-reference handling (& pronoun handling and normalization of entities) before visualization.
    #   - resolve coreference cases like "Seldon" or "Foundation"
    # - measure the quality
    # - One or more visualizations. Word Cloud does not count as a visualization!
    #   - Custom Mapping: https://melaniewalsh.github.io/Intro-Cultural-Analytics/Mapping/Custom-Maps.html
    # - Detecting anomalies gets you bonus points
    # - Creating a great video with audio also gets you bonus points
