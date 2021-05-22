from config import FoundationTrilogy
from preprocess import preprocess
from ner import NER
from entity_connections import LINK_ENTITIES
from visualization import CHARACTER_NETWORK

if __name__ == '__main__':

    text = FoundationTrilogy[:-1200000]
    #text = FoundationTrilogy
    parsed_list = preprocess(text, True)  # vector of preprocessed sentences
    people_list, location_list, predicted = NER(parsed_list, STAGE=True, VALIDATE=True)
    #TODO: Validation

    #TODO: CR + link with predicted
    people_links, location_links = LINK_ENTITIES(people_list, location_list, parsed_list, predicted, True)
    CHARACTER_NETWORK(people_links, True)

    #TODO: geo-mapping with location_links




    # TODO: EXTRA bonus points
    #   - Detecting anomalies gets you bonus points
    #   - Creating a great video with audio also gets you bonus points
