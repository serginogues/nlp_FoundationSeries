from config import FoundationTrilogy
from preprocess import preprocess
from ner import NER
from entity_connections import LINK_ENTITIES
from normalization import normalize_list

if __name__ == '__main__':

    text = FoundationTrilogy
    parsed_list = preprocess(text)  # vector of preprocessed sentences
    predicted = NER(parsed_list)

    people_links, location_links, events = LINK_ENTITIES(parsed_list, predicted)
    people_links = normalize_list(people_links)
