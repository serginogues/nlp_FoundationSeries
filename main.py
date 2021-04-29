"""
https://arxiv.org/pdf/1907.02704.pdf
1) The identification of characters. We distinguish two substeps:
    - Detect occurrences of characters in the narrative
        -  a character can appear under three forms in text: proper noun, nominal, and pronoun.
    - Unify these occurrences, i.e. to determine which ones correspond to the same character.
    In a text, the same character can appear under different names.
    The output of this step takes the form of a chronological sequence of unified character occurrences.

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

from entity_identification import *

Test_locations = [('Trantor', 7), ('Synnax', 2), ('Kalgan', 2), ('Arcturus', 1), ('Ahctuwus', 1), ('Anacreon', 1), ('Askone', 1), ('Radole', 1), ('Dellcass', 1), ('Haven', 1), ('Gentri', 1), ('Rossem', 1), ('Space under Foundation', 1)]
Test_people = [('Darell', 78), ('Seldon', 45), ('Barr', 44), ('Bayta', 41), ('Mallow', 40), ('Fie', 31), ('Hardin', 29), ('Toran', 28), ('Gaal', 26), ('Anthor', 22), ('Stettin', 22), ('Mis', 21), ('Dorwin', 20), ('Channis', 19), ('Munn', 18), ('Pritcher', 15), ('Mule', 15), ('Speaker', 15), ('Brodrig', 14), ('Arcadia', 14), ('Pirenne', 12), ('Sutt', 11), ('Pappa', 11), ('Randu', 10), ('Magnifico', 9), ('Indbur', 9), ('Turbor', 9), ('Verisof', 8), ('Wienis', 7), ('Ponyets', 7), ('Jael', 7), ('Forell', 7), ('Sermak', 6), ('Lepold', 6), ('Gorov', 6), ('Mayor', 5), ('Fara', 5), ('Master', 5), ('Commdor', 5), ('Riose', 5), ('Fran', 5), ('Kleise', 5), ('Mamma', 5), ('Lee', 4), ('Bort', 4), ('Pherl', 4), ('Chen', 3), ('Walto', 3), ('Aporat', 3), ('Fox', 3), ('Elders', 3), ('Student', 3), ('Semic', 3), ('Avakim', 2), ('Advocate', 2), ('Lameth', 2), ('Fulham', 2), ('Empire', 2), ('Orsy', 2), ('Foundation', 2), ('Capsule', 2), ('Iwo', 2), ('Mangin', 2), ('Ovall', 2), ('Hella', 2), ('Commason', 2), ('Plan', 2), ('Meirus', 2), ('Callia', 2), ('Poochie', 2), ('Palver', 2)]

if __name__ == '__main__':

    parsed_list = preprocess(FoundationTrilogy)
    people_list, people_list_df = entity_identification(parsed_list)
    #ToDo:
    # - negation handling, co-reference & pronoun handling and normalization of entities before visualization.
    # - measure the quality
    # - One or more visualizations. Word Cloud does not count as a visualization!
    # - Detecting anomalies gets you bonus points
    # - Creating a great video with audio also gets you bonus points
