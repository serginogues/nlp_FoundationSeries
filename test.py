from utils import *
from entity_identification import preprocess, detect_location
from correference_resolution import *

test = """The best existing authority we have for the details of his life is the biography written by Gaal 
Dornick who, as a young man, met Seldon two years before the great mathematician's death. 
The story of the meeting"""

parsed_list = preprocess(test)
people_list = ['Darell',  'Seldon',  'Barr',  'Bayta',  'Mallow',  'Fie',  'Gaal',  'Hardin',  'Toran',  'Anthor',  'Stettin',  'Mis',  'Dorwin',  'Munn',  'Channis',  'Pritcher',  'Arcadia',  'Brodrig',  'Mule',  'Speaker',  'Pirenne',  'Pappa',  'Sutt',  'Randu',  'Indbur',  'Turbor',  'Magnifico',  'Verisof',  'Wienis',  'Commdor',  'Jael',  'Sermak',  'Lepold',  'Forell',  'Mayor',  'dryly',  'Kleise',  'Mamma',  'Chen',  'Fara',  'Lee',  'Bort',  'Master',  'Pherl',  'Fran',  'Semic',  'Walto',  'Aporat',  'Sir',  'Gorov',  'Fox',  'Elders',  'Palver',  'Avakim',  'Advocate',  'Lameth',  'Fulham',  'Empire',  'Gorm',  'Ponyets',  'Emperor',  'Riose',  'Foundation',  'Devers',  'Dad',  'Capsule',  'Iwo',  'Ovall',  'Hella',  'Commason',  'Plan',  'Student',  'Meirus',  'Poochie']

coreference_resolution(people_list, parsed_list)

