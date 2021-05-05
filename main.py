from preprocess import *
from ner import named_entity_recognition
from cr import get_full_named_entities
from entity_connections import find_entity_links
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
Done = False
InProgress = False

if __name__ == '__main__':

    if Done:
        parsed_list = preprocess(FoundationTrilogy)
        people_list, location_list = named_entity_recognition(parsed_list)
        final_list = get_full_named_entities(people_list, parsed_list)  # chronological sequence of unified character occurrences
    else:
        final_list = [['Arkady Darell'], ['Hari Seldon'], ['Raven Seldon'], ['Fiari Seldon'], ['Seldon Hardin'], ['Ducem Barr'], ['Onum Barr'], ['Bayta Darell'], ['Hober Mallow'], ['Fie'], ['Gaal Dornick'], ['Salvor Hardin'], ['Toran Darell'], ['Pelleas Anthor'], ['Stettin'], ['Ebling Mis'], ['Dorwin'], ['Homir Munn'], ['Flomir Munn'], ['Bail Channis'], ['Han Pritcher'], ['Flan Pritcher'], ['Arcadia Darell'], ['Brodrig'], ['The Mule'], ['Speaker'], ['Lewis Pirenne'], ['Pappa'], ['Jorane Sutt'], ['Randu'], ['Indbur'], ['Jole Turbor'], ['Magnifico Giganticus'], ['Verisof'], ['Wienis'], ['Commdor Asper'], ['Ankor Jael'], ['Sef Sermak'], ['Lepold'], ['Sennett Forell'], ['Mayor Hardin'], ['dryly'], ['Kleise'], ['Mamma'], ['Linge Chen'], ['Jord Fara'], ['Yohan Lee'], ['Lee Senter'], ['Lewis Bort'], ['Master'], ['Pherl'], ['Fran'], ['Elvett Semic'], ['Walto'], ['Theo Aporat'], ['Eskel Gorov'], ['Fox'], ['Elders'], ['Preem Palver'], ['Avakim'], ['Advocate'], ['Lameth'], ['Fulham'], ['Galactic Empire'], ['Second Empire'], ['Les Gorm'], ['Limmar Ponyets'], ['Emperor'], ['Bel Riose'], ['Second Foundation'], ['Second Foundationer'], ['First Foundation'], ['Lathan Devers'], ['Dad'], ['Capsule'], ['Iwo'], ['Ovall Gri'], ['Hella'], ['Jord Commason'], ['Plan'], ['Student'], ['Lev Meirus'], ['Poochie']]
    # Up to here the code works perfect

    if InProgress:
        links_list = find_entity_links(final_list, FoundationTrilogy)
    else:
        links_list = [[['Second Foundation'], ['First Foundation'], 188],  [['The Mule'], ['Randu'], 166],  [['The Mule'], ['Bail Channis'], 91],  [['Pelleas Anthor'], ['Arkady Darell'], 83],  [['Galactic Empire'], ['Second Empire'], 73],  [['Jorane Sutt'], ['Hober Mallow'], 69],  [['Hari Seldon'], ['Plan'], 67],  [['Galactic Empire'], ['Bel Riose'], 66],  [['Bel Riose'], ['Lathan Devers'], 64],  [['Ebling Mis'], ['Indbur'], 63],  [['Wienis'], ['Lepold'], 51],  [['Jole Turbor'], ['Elvett Semic'], 51],  [['Seldon Hardin'], ['Salvor Hardin'], 45],  [['Hari Seldon'], ['Fie'], 38],  [['Seldon Hardin'], ['Lewis Pirenne'], 37],  [['Galactic Empire'], ['Emperor'], 33],  [['Speaker'], ['Fie'], 31],  [['Brodrig'], ['Emperor'], 30],  [['Homir Munn'], ['Flomir Munn'], 26],  [['Hober Mallow'], ['Ankor Jael'], 25],  [['Indbur'], ['Second Foundation'], 24],  [['Pelleas Anthor'], ['Kleise'], 24],  [['Limmar Ponyets'], ['Master'], 22],  [['Jorane Sutt'], ['Jord Fara'], 20],  [['Fran'], ['Randu'], 20],  [['Yohan Lee'], ['Sef Sermak'], 18],  [['Les Gorm'], ['Eskel Gorov'], 18],  [['Student'], ['Speaker'], 18],  [['Mamma'], ['Pappa'], 18],  [['Han Pritcher'], ['Flan Pritcher'], 16],  [['Fie'], ['Yohan Lee'], 16],  [['Stettin'], ['The Mule'], 15],  [['Sennett Forell'], ['Hober Mallow'], 14],  [['Pappa'], ['Preem Palver'], 12],  [['Ducem Barr'], ['Onum Barr'], 11],  [['Verisof'], ['Mayor Hardin'], 11],  [['Pherl'], ['Master'], 11],  [['Dad'], ['Fran'], 11],  [['Dorwin'], ['Galactic Empire'], 10],  [['Hari Seldon'], ['Raven Seldon'], 9],  [['Sef Sermak'], ['Lewis Bort'], 9],  [['Capsule'], ['Limmar Ponyets'], 9],  [['The Mule'], ['Jord Commason'], 9],  [['Seldon Hardin'], ['Mayor Hardin'], 8],  [['Arkady Darell'], ['Bayta Darell'], 7],  [['Lev Meirus'], ['Poochie'], 7],  [['Sef Sermak'], ['Walto'], 6],  [['Yohan Lee'], ['Lee Senter'], 6],  [['Stettin'], ['Lev Meirus'], 6],  [['Arkady Darell'], ['Arcadia Darell'], 5],  [['Advocate'], ['Hari Seldon'], 5],  [['Fran'], ['Second Foundationer'], 5],  [['Second Foundation'], ['Ovall Gri'], 5],  [['Fox'], ['Han Pritcher'], 5],  [['Avakim'], ['Hari Seldon'], 4],  [['Hari Seldon'], ['Linge Chen'], 4],  [['Seldon Hardin'], ['dryly'], 4],  [['Pherl'], ['Elders'], 4],  [['Arkady Darell'], ['Toran Darell'], 3],  [['Hari Seldon'], ['Fiari Seldon'], 3],  [['Gaal Dornick'], ['Hari Seldon'], 3],  [['Jord Fara'], ['Fulham'], 3],  [['Les Gorm'], ['Second Foundation'], 3],  [['Second Foundation'], ['Commdor Asper'], 3],  [['Wienis'], ['Theo Aporat'], 2],  [['Second Foundation'], ['Magnifico Giganticus'], 2],  [['Fran'], ['Iwo'], 2],  [['Raven Seldon'], ['Fiari Seldon'], 1],  [['Bayta Darell'], ['Toran Darell'], 1],  [['Bayta Darell'], ['Arcadia Darell'], 1],  [['Salvor Hardin'], ['Mayor Hardin'], 1],  [['Toran Darell'], ['Arcadia Darell'], 1],  [['Seldon Hardin'], ['Lameth'], 1]]
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
