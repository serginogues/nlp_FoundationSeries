from config import STAGE
from preprocess import preprocess
from ner import named_entity_recognition
from ne_complete_names import get_full_named_entities
from entity_connections import find_entity_links_and_events
from visualization import super_network

"""
*********PIPELINE*********
0 - preprocess.py           - preprocess()                  - DONE
1 - ner.py                  - named_entity_recognition()    - DONE
2 - ne_complete_names.py    - get_full_named_entities()     - DONE
3 - CR + ALIAS RESOLUTION
4 - CR + ENTITY RELATIONS
5 - NORMALIZATION
6 - VISUALIZATION
7 - QUALITY VALIDATION
"""

final_list = [['Arkady Darell'], ['Hari Seldon'], ['Seldon Crisis'], ['Raven Seldon'], ['Ducem Barr'],
                      ['Onum Barr'], ['Bayta Darell'], ['Hober Mallow'], ['Trader Mallow'], ['Flober Mallow'], ['Fie'],
                      ['Salvor Hardin'], ['Toran Darell'], ['Gaal Dornick'], ['Pelleas Anthor'], ['Stettin'],
                      ['Ebling Mis'], ['Dorwin'], ['Bail Channis'], ['Homir Munn'], ['Flomir Munn'], ['Han Pritcher'],
                      ['Flan Pritcher'], ['General Pritcher'], ['Mule'], ['First Speaker'], ['Arcadia Darell'],
                      ['Brodrig'], ['Pirenne'], ['Jorane Sutt'], ['Tomaz Sutt'], ['Pappa'], ['Randu'],
                      ['Magnifico Giganticus'], ['Indbur'], ['Jole Turbor'], ['Poly Verisof'], ['Wienis'],
                      ['Limmar Ponyets'], ['Ankor Jael'], ['Sennett Forell'], ['Sef Sermak'], ['Lepold I'],
                      ['Eskel Gorov'], ['Callia'], ['Mayor Hardin'], ['Jord Fara'], ['Grand Master'], ['Master Trader'],
                      ['Bel Riose'], ['Fran'], ['Kleise'], ['Mamma'], ['Yohan Lee'], ['Lee Senter'], ['Lewis Bort'],
                      ['Pherl'], ['Linge Chen'], ['Walto'], ['Theo Aporat'], ['Fox'], ['Elders'], ['Student'],
                      ['Elvett Semic'], ['Avakim'], ['Advocate'], ['Lameth'], ['Yate Fulham'], ['Galactic Empire'],
                      ['Second Empire'], ['First Empire'], ['Orsy'], ['Second Foundation'], ['First Foundation'],
                      ['Encyclopedia Foundation'], ['Personal Capsule'], ['Iwo'], ['Mangin'], ['Ovall Gri'], ['Hella'],
                      ['Jord Commason'], ['Plan'], ['Lev Meirus'], ['Poochie'], ['Preem Palver']]

if __name__ == '__main__':

    parsed_list = preprocess()  # vector of preprocessed sentences

    people_list, location_list = named_entity_recognition(parsed_list)

    final_list = get_full_named_entities(people_list, parsed_list)  # Final List of characters

    # Up to here the code works perfect
    #TODO:
    # - Alias resolution - pattern: PERSON + ["known as" OR ", "
    # - Entity Relations (ideas in course 5 diapo 34)
    # - Coreferences for entity connection
    # - Use normalization of extracted entities before visualization
    # - Visualization:
    #   - Custom Mapping with https://melaniewalsh.github.io/Intro-Cultural-Analytics/Mapping/Custom-Maps.html
    #   - Events: see course 5 slide 47 (tree graph)
    # - Measure Quality:
    #   - Do a random validation of quality, avoid to blindly apply libraries without understanding
    #   how they work or what the quality is. So, the need to measure that by a small (50-100) random manual validations.
    #   - Also incorporate multi-juror validation and calculate a kappa distance in the above

    links_list = find_entity_links_and_events(final_list, parsed_list)

    if STAGE > 6:
        super_network(links_list)

    # TODO: EXTRA bonus points
    #   - Detecting anomalies gets you bonus points
    #   - Creating a great video with audio also gets you bonus points
