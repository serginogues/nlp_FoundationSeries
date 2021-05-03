from utils import *
from correference_resolution import *

test = """My dad entered to the room and smiled. "How are you?" he said. "I am fine John" I answered. """
people_list = ['Darell',  'Seldon',  'Barr',  'Bayta',  'Mallow',  'Fie',  'Gaal',  'Hardin',  'Toran',  'Anthor',  'Stettin',  'Mis',  'Dorwin',  'Munn',  'Channis',  'Pritcher',  'Arcadia',  'Brodrig',  'Mule',  'Speaker',  'Pirenne',  'Pappa',  'Sutt',  'Randu',  'Indbur',  'Turbor',  'Magnifico',  'Verisof',  'Wienis',  'Commdor',  'Jael',  'Sermak',  'Lepold',  'Forell',  'Mayor',  'dryly',  'Kleise',  'Mamma',  'Chen',  'Fara',  'Lee',  'Bort',  'Master',  'Pherl',  'Fran',  'Semic',  'Walto',  'Aporat',  'Sir',  'Gorov',  'Fox',  'Elders',  'Palver',  'Avakim',  'Advocate',  'Lameth',  'Fulham',  'Empire',  'Gorm',  'Ponyets',  'Emperor',  'Riose',  'Foundation',  'Devers',  'Dad',  'Capsule',  'Iwo',  'Ovall',  'Hella',  'Commason',  'Plan',  'Student',  'Meirus',  'Poochie']

parsed = nlp(test)
print("All references", pronoun_references(parsed))
print("All mentions", all_mentions(parsed))


