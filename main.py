from config import FoundationTrilogy
from preprocess import preprocess
from ner import NER
from entity_connections import LINK_ENTITIES
from normalization import normalize_list
from visualization import CHARACTER_NETWORK

if __name__ == '__main__':

    #text = FoundationTrilogy[:-1200000]
    text = FoundationTrilogy
    parsed_list = preprocess(text, False)  # vector of preprocessed sentences
    predicted = NER(parsed_list, STAGE=False)

    #TODO: CR
    people_links, location_links = LINK_ENTITIES(parsed_list, predicted, True)
    normalize, people_links = normalize_list(people_links, True)
    #TODO: normalize
    CHARACTER_NETWORK(people_links, True)

    #TODO: geo-mapping with location_links

    # TODO: EXTRA bonus points
    #   - Detecting anomalies gets you bonus points
    #   - Creating a great video with audio also gets you bonus points
