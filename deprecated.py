from config import *

entities = [['Arkady Darell'], ['Hari Seldon'], ['Seldon Plan'], ['Seldon Crisis'], ['Raven Seldon'],
                      ['Seldon Convention'], ['Ducem Barr'], ['Onum Barr'], ['Bayta Darell'], ['Hober Mallow'],
                      ['Trader Mallow'], ['Flober Mallow'], ['Extinguishing Field'], ['Field Bearings'],
                      ['Salvor Hardin'], ['Toran Darell'], ['Gaal Dornick'], ['Pelleas Anthor'], ['Stettin'],
                      ['Ebling Mis'], ['Miss Erlking'], ['Dorwin'], ['Bail Channis'], ['Homir Munn'], ['Flomir Munn'],
                      ['Captain Pritcher'], ['Han Pritcher'], ['Flan Pritcher'], ['Colonel Pritcher'],
                      ['General Pritcher'], ['Mule'], ['First Speaker'], ['Arcadia Darell'], ['Brodrig'], ['Pirenne'],
                      ['Jorane Sutt'], ['Tomaz Sutt'], ['Pappa'], ['Randu'], ['Magnifico Giganticus'], ['Indbur'],
                      ['Jole Turbor'], ['Poly Verisof'], ['Wienis'], ['Limmar Ponyets'], ['Ankor Jael'],
                      ['Sennett Forell'], ['Sef Sermak'], ['Lepold I'], ['Eskel Gorov'], ['Callia'], ['Mayor Indbur'],
                      ['Mayor Hardin'], ['Jord Fara'], ['Grand Master'], ['Master Trader'], ['Bel Riose'],
                      ['General Riose'], ['Fran'], ['Kleise'], ['Mamma'], ['Yohan Lee'], ['Lee Senter'], ['Lewis Bort'],
                      ['Pherl'], ['Linge Chen'], ['Walto'], ['Theo Aporat'], ['Fox'], ['Elders'], ['Student'],
                      ['Elvett Semic'], ['Avakim'], ['Advocate'], ['Lameth'], ['Yate Fulham'], ['Galactic Empire'],
                      ['Second Empire'], ['First Empire'], ['Orsy'], ['Second Foundation'], ['First Foundation'],
                      ['Second Foundationer'], ['Encyclopedia Foundation'], ['Second Foundationers'],
                      ['Foundation Number'], ['Personal Capsule'], ['Iwo'], ['Mangin'], ['Ovall Gri'], ['Hella'],
                      ['Jord Commason'], ['Plan'], ['Lev Meirus'], ['Poochie'], ['Preem Palver']]

text = """Bayta's first sight of Haven was entirely the contrary of spectacular. Her husband pointed it out 
- a dull star lost in the emptiness of the Galaxy's edge. It was past the last sparse clusters, to 
where straggling points of light gleamed lonely. And even among these it was poor and inconspicuous. 
Toran was quite aware that as the earliest prelude to married life, 
the Red Dwarf lacked impressiveness and his lips curled self-consciously. "I know, Bay - It isn't exactly a proper 
change, is it? I mean from the Foundation to this." "A horrible change, Toran. I should never have married you."""


def token_is_candidate(token):
    """
    :return: True if token is proper name or adjective
    """
    if token.pos_ == 'PROPN' or token.pos_ == 'ADJ' and str(token) not in honorific_words:
        return True
    else:
        return False


def print_results_and_sort(entity_list, connection_list):
    for i, name in enumerate(entity_list):
        conn = [x for x in connection_list if name[0] in x]
        print(i, "-", name[0], len(conn), "list: ", conn)

    def takethird(elem):
        return elem[2]

    connection_list.sort(key=takethird, reverse=True)

    return connection_list
