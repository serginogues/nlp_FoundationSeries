"""
Rule-Based Named Entity Recognition model for the detection of character occurrences
"""
from config import tqdm, Counter, honorific_words, person_verbs, matcher, location_name_pattern, location_name, \
    travel_to_pattern, travel_to_verbs, nlp, punctuation_tokens
from utils import get_ents_from_doc


def get_full_name(doc, token):
    full_name = [x for x in doc.ents if str(token) in str(x) and len(x) > 1]
    if len(full_name) > 0:
        return full_name[0]
    else:
        return token.text


def named_entity_recognition(sentence_list, STAGE=True):
    """
    :return: chronological sequence of unified character and location occurrences
    """
    print("Start NER")
    if STAGE:
        main_characters_ = []
        locations_ = []
        unclassified = []
        for i in tqdm(range(len(sentence_list))):
            doc = sentence_list[i]
            ents = get_ents_from_doc(doc)
            ents = list(set([x for x in ents if len(x) > 2 and not x.islower() and not x.isupper()]))
            if any(ents):
                for name in ents:
                    list_ = [x for x in doc for y in name.split(" ") if str(x) == y]
                    if len(list_) > 1:
                        token = list_[1]
                    else:
                        token = list_[0]
                    if ner_person(doc, token):
                        main_characters_.append(name)

                    elif ner_location(doc, token):
                        locations_.append(name)
                    else:
                        unclassified.append(name)

        location_list = list(set(locations_))
        people_list = list(set([x for x in main_characters_ if len(x) > 2]))
        for ent in people_list:
            if any([x for x in punctuation_tokens if x in ent]):
                people_list.remove(ent)
        unclassified = list(set(unclassified))
        unclassified = [x for x in unclassified if (x not in people_list and x not in location_list)]
        for ent in unclassified:
            if any([x for x in punctuation_tokens if x in ent]):
                unclassified.remove(ent)

    else:
        location_list = ['Space',
                         'Neotrantor',
                         'Kalgan',
                         'Arcturus',
                         'Dellcass',
                         'Trantor',
                         'Haven',
                         'Gentri',
                         'Anacreon',
                         'Terminus',
                         'Synnax',
                         'Ahctuwus',
                         'Rossem',
                         'Askone',
                         'Radole']
        people_list = ['Salvor',
                       'Haut Rodric',
                       'Homir',
                       'Gorov',
                       'Lieutenant Dirige',
                       'Indbur',
                       'Twice Pritcher',
                       'Pirenne',
                       'Ponyets',
                       'Tinter',
                       'Meirus',
                       'Personal Capsule',
                       'Elvett Semic',
                       'Asper',
                       'Pherl',
                       'Whew',
                       'Munn',
                       'Callia',
                       'Board',
                       'Hari Seldon',
                       'Privy Secretary',
                       'Lepold',
                       'Amann',
                       'Homir Munn',
                       'Argo',
                       'Lameth',
                       'Yate Fulham',
                       'Dornick',
                       'Asper Argo',
                       'First Speaker',
                       'Hardin',
                       'Dixyl',
                       'Siwennian',
                       'Bort',
                       'End',
                       'Crast',
                       'Dad',
                       'Uncle Homir',
                       'Rodric',
                       'Master',
                       'Empire',
                       'Tippellum',
                       'Lewis',
                       'Sammin',
                       'Fie',
                       'Senter',
                       'Randu',
                       'Verisof',
                       'Turbor',
                       'Student',
                       'Forell',
                       'Mis',
                       'Jole Turbor',
                       'Jerril',
                       'Orsy',
                       'Bayta',
                       'Far Star',
                       'Ovall',
                       'Avakim',
                       'Dirige',
                       'Tomaz Sutt',
                       'Hober Mallow',
                       'Aporat',
                       'Twer',
                       'Cleon II',
                       'Toran',
                       'Flan',
                       'Fleadquarters',
                       'Magnifico',
                       'Hotel',
                       'Sennett Forell',
                       'Stettin',
                       'Lundin Crast',
                       'Fara',
                       'Pritcher',
                       'Elders',
                       'Sutt',
                       'Haven',
                       'Bel',
                       'Second Foundation',
                       'Grand Master',
                       'Barr',
                       'Wienis',
                       'Lee',
                       'Councilman',
                       'Lee Senter',
                       'Hella',
                       'Pappa',
                       'Star',
                       'Lathan Devers',
                       'Supervisor',
                       'Riose',
                       'Chairman',
                       'Salvor Hardin',
                       'Channis',
                       'Poochie',
                       'Dorwin',
                       'Ebling Mis',
                       'Han',
                       'Korell',
                       'Ducem Barr',
                       'Linge Chen',
                       'Fox',
                       'Semic',
                       'Darell',
                       'Anthor',
                       'First',
                       'Mangin',
                       'Brodrig',
                       'Askonian',
                       'Pelleas Anthor',
                       'Commissioners',
                       'Walto',
                       'Commissioner',
                       'Speaker',
                       'Foundation',
                       'Space',
                       'Fulham',
                       'Galactography',
                       'Gorm',
                       'Bail Channis',
                       'Seldon',
                       'Juddee',
                       'Iwo',
                       'Mamma',
                       'Commason',
                       'Chen',
                       'Arcadia',
                       'Bel Riose',
                       'Fran',
                       'Transmitter',
                       'Les Gorm',
                       'Jaim Twer',
                       'Mallow',
                       'Palver',
                       'Dagobert IX',
                       'Radolian',
                       'Secretary',
                       'Flober Mallow',
                       'Mule',
                       'Capsule',
                       'Erlking',
                       'Advocate',
                       'Gaal',
                       'Devers',
                       'Jael',
                       'Luxor Hotel',
                       'Kleise',
                       'Lieutenant Tinter',
                       'Elvett',
                       'Sermak',
                       'Emperor',
                       'Kalganese']
        unclassified = ['Madame', 'Preem Palver', 'Revolutionary', 'Number One', 'Bayta Darell', 'Kid', 'Sun',
                        'Arcadia Palver', 'Yohan Lee', 'Veneration', 'Kinglet', 'Great Galaxy', 'Trading Worlds',
                        'Bearings Works', 'Lem', 'Damnedest', 'Reverend', 'Stannell', 'Education', 'Worlds',
                        'Obligations', 'Snake', 'Great Interregnum', 'New', 'Independent Traders', 'Jorane', 'Jeppson',
                        'Flold', 'Second Foundationers', 'Pelleas', 'Imperial Seal', 'Guard', 'Birds', 'Poor',
                        'Rossemites', 'Way', 'Coronation', 'Engineer Orre', 'Reception', 'Opposing', 'Cenn', 'Piwenne',
                        'Ambassador', 'Jumps', 'Shop', 'Peurifoy', 'Anxiety', 'Imperial Majesty', 'Year', 'Thou',
                        'Old Kingdoms', 'Levvaw', 'Base', 'Naval', 'Yes-', 'Kalgan Palace', 'Santanni',
                        'East Peninsula', 'Era', 'York City', 'Adam', 'Preem', 'Radole City', 'Representative', 'Hyper',
                        'Sciences', 'Whassallian', 'Janet Jeppson', 'Royal', 'Galactic Spirit', 'Fifty', 'Days',
                        'Psyc/7ohistorical', 'MULE Second', 'Peasant Rossem', 'Field Region', 'March', 'Lors Avakim',
                        'Edition', 'Wiscard', 'Trader', 'Vrank', 'Entun', 'Frankly', 'Actionist Party', 'Third',
                        'Indicator', 'Massena', 'Smushyk', 'Summer Planets', 'Court', 'Flowered Path', 'Prince Regent',
                        'Poo', 'Paradise', 'National Fleet', 'Symes', 'Army', 'Galactic Sector', 'Executive Council',
                        'Kleeno Nuclear', 'Old Trantor', 'Lieutenant', 'Doctah Piwenne', 'Image', 'Hmp', 'Offensive',
                        'Mediator Extraordinary', 'Converted', 'Asperta', 'wispy Lens', 'echoed Twer', 'Smyrnian',
                        'Plan', 'Foundation Convention', 'Jord Parma', 'Previous Enclosure', 'Except-', 'Squadron',
                        'Noth', 'Chief', 'Engine', 'Seal', 'Psychological', 'Libwawy', 'Newton', 'Nebula',
                        'reborn Foundation', 'Trading', 'Citizenship', 'Speakers', 'Red Dwarf', 'Lundin', 'Majesty',
                        'Tenth', 'Onum Barr', 'Sectors', 'Planetary', 'Balance', 'Grand Mastership', 'Planets', 'Eskel',
                        'Imperial Court', 'Tamper', 'Hoik', 'SONOR Ebling', 'Willig', 'Path', 'Jump', 'National',
                        'Poof', 'Obijasi', 'Rossemite', 'Creation', 'prefect Anselm', 'First Theorem', 'Power', 'Works',
                        'Inertia', 'Argolid Temple', 'Extinguishing', 'Boston University', 'Thefutureofseldonsplan',
                        'Historical Necessity', 'Jorane Sutt', 'Second Galactic', 'Dominions', 'Second Foundationism',
                        'War Department', 'Flow', 'Terminus City', 'Democratic', 'Theater', 'Prefect',
                        'EnvoyExtraordinary', 'Tarki', 'Revered', 'Grand Fleet', 'Hardin Building', 'Chens', 'Probe',
                        'Lem Tarki', 'Orre', 'Seldom', 'Church', 'Steffani', 'Smyrno', 'Mankind', 'Police Lieutenant',
                        'Gnome Press', 'Armada', 'Commission', 'Psychology Reference', 'Cosker', 'Bood', 'Onum',
                        'Cards', 'Theo', 'February', 'Good Old', 'New York', 'Thallos', 'Mental Science', 'Milky',
                        'Gilmer', 'Beloved', 'Imperial Palace', 'Beard', 'Search', 'Gri', 'Vandyke', 'Mules',
                        'Lemul Cluster', 'South', 'Mallow Hall', 'Engineer', 'dragoon Randu', 'Holy Food',
                        'Channis taut', 'Chambers', 'Barbarism', 'Arcadia sf/7/', 'Stanmark', 'Great Birds',
                        'Border Fleet', 'Riot', 'Vault', 'Lefkin', 'Characteristics', 'Imperials', 'Mediator',
                        'Excellence', 'Narovi', 'Publis', 'Trantor Imperial', 'Halls', 'hugest Empire', 'Hierarchy',
                        'Extraordinary', 'Zeonian', 'Parma', 'One', 'Galactica Publishing', 'Moro', 'Muller Hoik',
                        'Analytical', 'Kalganids', 'Bay', 'Nuclear', 'First Minister', 'Goddess', 'Jan Smite',
                        'Radole Tribune', 'Tazenda', 'Bor Alurin', 'Citizen', 'Merchant', 'Border', 'Lords', 'Probes',
                        'Filia', 'Trade Fleet', 'Minister', 'Gnome', 'Stanel', 'Peasant', 'Boston', 'Garre', 'f Les',
                        'Peninsula', 'Iwo Lyon', 'Orsha', 'Franssart', 'Number', 'First Galactic',
                        'Intergalactic Standard', 'Malignant', 'Superficial', 'Planetary Police', 'Mental Static',
                        'Pardon', 'GALACTICA.Gaal', 'Black Space', 'Outer Provinces', 'Tenth Fleet', 'Futility',
                        'Red Stars', 'Yohan', 'Nuclear Washing', 'Second', 'Composition', 'Temporal', 'Follow',
                        'Han Pritcher', 'Grun', 'Fiari Seldon', 'Sarnia', 'Stannel', 'Eli', 'Central Sectors', 'Orum',
                        'Axis', 'Foundation Traders', 'Good', 'Chamber', 'INTERLUDE Bail', 'Fourth', 'Sergeant',
                        'Muller', 'Late', 'Point', 'Ahh', 'Imperial Police', 'Institutes', 'Gentlemen',
                        'Zeonian Rebellion', 'Doc', 'Horleggor', 'Arkady Darell', 'Analytical Rule', 'Poor Ebling',
                        'Secret Police', 'Consulate', 'Wispy', 'Ricker', 'Author', 'Commdora', 'Dwarf', 'World Trantor',
                        'Conventions', 'Extinguishing Field', 'blazed Toran', 'Imperial Capital', 'Hardin dryly',
                        'Merchant Princes', 'Anacreonian', 'Chamberlain', 'Imperial Coronation', 'Three', 'Flelicon',
                        'Limmar', 'Eskel Gorov', 'Grand Opening', 'Enemy', 'Voice', 'Machines', 'Transmitting Station',
                        'Await', 'Palley', 'Province', 'GALACTICA.Lewis Pirenne', 'Psychohistory', 'Press', 'Chair',
                        'Empiah', 'Galactic Empires', 'Ammenetik', 'Imperial University', 'Throne', 'Crisis', 'Temple',
                        'Visual', 'Imperial navy', 'Academy', 'Noble', 'Impasse', 'Upshur', 'Grounds', 'Empires',
                        'Depresser', 'Central School', 'Red Corridor', 'Orders', 'Excellency', 'Dear Father',
                        'Anselm Haut', 'Poly Verisof', 'Visual Record', 'Jaim', 'Asimov', 'PEASANT Third', 'Zoranel',
                        'Free Trade', 'Filian', 'GALACTICA.Bayta', 'Group', 'Protect', 'Flan Pritcher', 'Enclosure',
                        'Guards', 'Council', 'Spaceport', 'Imperial Government', 'Foundation Era', 'Stannell VI',
                        'Neurochemical Electromathematics', 'Slide', 'Standard Time', 'Cosmos', 'Giganticus', 'Tech',
                        'Luxor', 'Realm', 'Imperial Cruiser', 'Glyptal', 'Red', 'Second Foundationer', 'Upstairs',
                        'Journal', 'Action', 'High', 'Planet', 'Slide Rule', 'Universe', 'Dokor Walto', 'Plateau',
                        'United', 'Cruiser', 'Static', 'Leffert', 'Energy Transmitting', 'Lens Image', 'Warm', 'The',
                        'FHardin', 'Revered Jord', 'Minister Lev', 'Four', 'Meeting Hall', 'Secret Service', 'Anselm',
                        'Main', 'Outskirts', 'Mind Static', 'Old', 'Headstrong', 'Silver', 'Dark', 'Outer', 'Kings',
                        'Daluben', 'Tender', 'Ahctuwian', 'Fennel', 'Haut', 'Party', 'Free', 'Silver Star', 'Jaim Orsy',
                        'Mores', 'Phase', 'Doctah', 'Formality', 'Regent', 'Miran', 'Third Class', 'Puissant Majesty',
                        'Milla', 'Interregnum', 'Stannel V', 'Kamble', 'Convention', 'Elder', 'Patrician',
                        'Channel Drive', 'Seldon Historical', 'Vincetori', 'Temples', 'Meeting', 'Lyon', 'Fall',
                        'Second Empire', 'Jord', 'Owigin Question', 'Expedition', 'Viewer', 'Foundational',
                        'Olynthus Dam', 'Raven', 'Ruin', 'Mastership', 'Empewah', 'Nationalism', 'Dark Stars',
                        'Days Fight', 'Eastern Spaceport', 'Spirit', 'Reference Room', 'Alpha Centauwi', 'Suit',
                        'Imperial Library', 'Actionist', 'Senior', 'Pax', 'flared Bayta', 'Yes- Yes-', 'Heroic', 'Bobo',
                        'Union', 'Anacreonians', 'Counsellor', 'Region', 'Tomma', 'First Empire', 'Democrat',
                        'whereupon Toran', 'Renascence', 'Galactic Paradise', 'Trading Representative', 'Library',
                        'Blue Drift', 'Qualified Technician', 'Periphery', 'Executive Offices', 'Necessity', 'Whispers',
                        'Flis', 'Domain', 'Central Library', 'Engineer Huxlani', 'Mat', 'Administrator', 'Governors',
                        'Fight', 'Imperialpolicy', 'Imperial conquest', 'Chancellor', 'Stowaway',
                        'Foundation Consulate', 'Proceedings', 'Building', 'Emotional Repulsion', 'Hahdin',
                        'Salvor FHardin', 'Foundation Navy', 'Route Handbook', 'Flomir Munn', 'Ahctuwian System',
                        'Tyrant Indbur', 'Nyak', 'Research Institutes', 'Distorter', 'Normannic Sector', 'Flaven',
                        'Jole', 'Council Chamber', 'Seldon Commission', 'Locrian', 'Oligarchy', 'Tribes', 'HAND Bel',
                        'Foundations', 'Cabinet', 'Siwenna', 'Levi', 'Puissant', 'Lieutenant Drawt', 'Heroic Age',
                        'Cil', 'Theorem', 'Bonde', 'Neotrantorlan', 'Provinces', 'Time Capsule', 'Iss', 'New Trantor',
                        'Demen', 'Trader Mallow', 'Cleon', 'Nightfall', 'United States', 'Emperors', 'Cause',
                        'Admiralty', 'Gamma Andromeda', 'Arkady', 'Intergalactic', 'Palvro', 'Master Trader',
                        'Korellian Republic', 'Fourth Interlude', 'Field', 'Treasury', 'School', 'Organ', 'Logic',
                        'Stiffly', 'Great Seldon', 'Officer', 'Scientist', 'Mind', 'Fwom', 'Jacquerie', '6th Edition',
                        'Plateaus', 'Courtiers', 'Corporation', 'Interlude', 'Tower', 'Fley', 'HariSeldon',
                        'gasped Palver', 'Slang', 'Sunwards', 'Cluster', 'ASIMOV Contents', 'Opposing Periphery',
                        'Kwomwill', 'Conspirators', 'Men', 'Imperial Age', 'Palace', 'Lost Cause', 'Imperium',
                        'Characteristic', 'Hazily', 'Avast', 'Democratic Underground', 'Mathematicians', 'Fields',
                        'Neurochemical', 'Prophet Hari', 'Senior Lieutenant', 'Food', 'Republic', 'Man', 'Day',
                        'Shield', 'pow T', 'Eastern', 'Trash', 'Gleen', 'Anacweon', 'Spiritual Power', 'Daribow',
                        'Isaac Asimov', 'Biostatistics', 'Tomaz', 'Stanel VI', 'Smyrnians', 'Standard Year',
                        'Production', 'Hanto', 'Jaws', 'Hari Seldom', 'Psyc/7ohistorical Necessity', 'Foundationer',
                        'City', 'Armed', 'Argolid', 'Corridor', 'Previous', 'Cleon ll', 'Revered Parma', 'Verse',
                        'Association', 'Leemor', 'Sub', 'All', 'Prince Lefkin', 'Galactic Periphery', 'Insulin',
                        'Rhetoric', 'Stars', 'Factory', 'Memory', 'Seldon Fable', 'Publis Manlio', 'Encyclopedia',
                        'Development', 'Government', 'Drawt', 'Soviet Union', 'Under', 'Home Commissioner', 'Peace',
                        'Age', 'Hangar', 'Kleeno', 'Health', 'Freedom', 'Historical Sciences', 'Kalganian',
                        'Armed Forces', 'Trash Disinto', 'Brave', 'Outlander', 'Priest Poly', 'Information',
                        'Whatjasay', 'Twentieth', 'Bor', 'Contents PROLOGUE', 'Will', 'Orum Dirige', 'Fool', 'Police',
                        'Biochemistry', 'Wanda', 'Inner Kingdom', 'Sack', 'Inland Sea', 'Spirits', 'Co.', 'Kingdoms',
                        'Royal Governor', 'Siwennians', 'Viceroy', 'TRANTOR Devers', 'Folly', 'Psychologists',
                        'Flome Fleet', 'University', 'Andromeda', 'Detector', 'Sergeant Luk', 'Father',
                        'Psychostatistics', 'Question', 'Loris VI', 'Museum', 'Theah', 'Ponyet', 'Holy', 'Leaving',
                        'Summer', 'System', 'Divarts', 'Lera', 'Kiev', 'Psychic Probes', 'Treason', 'Park', 'Anacreon-',
                        'Trader Eskel', 'Askonians', 'Sonor', 'Fifth', 'Galaxy Protect', 'Shh', 'Milord',
                        'Kalgan- Kalgan', 'Mistress', 'Mobs', 'Kalganians', 'Fifth Speaker', 'Fennel Leemor', 'Alurin',
                        'Fable', 'Dagobert', 'Entuns', 'Traders', 'The Second', 'Foundation Number', 'Commander Yume',
                        'proceeded Randu', 'Hari', 'Stannells', 'Central', 'Thick Voice', 'City Charter', 'Repulsion',
                        'Sigma', 'Senator', 'First Foundation', 'Safety', 'Sun Room', 'Position', 'Muliana', 'Lucreza',
                        'Imperial Navy', 'Democrats', 'Technician', 'Public Safety', 'Cygni', 'Reverend Fathers',
                        'Stopped', 'Tamper Plateau', 'Uncle', 'Cerebellar', 'Lost', 'Raven Seldon', 'Siwius',
                        'Mathematics', 'Detention', 'Nation', 'Lemul', 'Time Vault', 'Anxiety Poli', 'Dewey', 'Janet',
                        'Imperial News', 'Poli', 'Propaganda', 'Haven II', 'Fleet', 'MULE First', 'yoah Foundation',
                        'Central Galaxy', 'Jord Commason', 'Purveyor', 'Torie', 'First Interlude', 'Hardinand',
                        'Cleon I', 'Flome', 'Damned', 'Hall Park', 'Engine Factory', 'Speakerhood', 'Soviet', 'Science',
                        'Mobs Riot', 'University Grounds', 'Phase Three', 'Combines', 'Korellian', 'Imperial Purple',
                        'Washing Machines', 'Peer', 'Analysis', 'Protocol', 'Galactic', 'Newton Bearings', 'Merit',
                        'Rule', 'Drive', 'Nyakbird', 'Galactica', 'Charter', 'Sef', 'Resonator', 'Debarkation Building',
                        'AUTHOR Isaac', 'Psychological Convention', 'Guild', 'Swords', 'Inner', 'Bail', 'Garden',
                        'Inland', 'Kingdom', 'Galactic Council', 'Norast', 'Outer Dominions', 'Madame Revolutionary',
                        'Sol', 'Navy', 'Malignant Spirit', 'Gaal Dornick', 'Foundation Fleet', 'Highness', 'Rely',
                        'Temporary Union', 'Grid TRANTOR', 'Royal Governors', 'City Journal', 'Inchney', 'Psychology',
                        'Mouth', 'Satiric', 'No- No-', 'BRIBERY Sergeant', 'Third Fleet', 'Engineer Third', 'Manlio',
                        'Flowered', 'Department', 'Grid', 'Public', 'Viceregal', 'Theo Aporat', 'Korellians', 'Wife',
                        'Hober', 'Service', 'Galaxy', 'Fle', 'Agriculture', 'Sector', 'Magnifico Giganticus',
                        'Galactic Offensive', 'Jawdun', 'Comets', 'Purple', 'Psychic Probe', 'Starlet', 'View', 'Room',
                        'Beloved Asper', 'Cyclopedia Square', 'Galloping', 'Transcriber', 'Yate', 'Radiant',
                        'Graybeard', 'Kalganid', 'Columbia', 'Mental', 'Home Squadron', 'Flomir', 'Gratitude',
                        'Fathers', 'Mineral', 'Encyclopedia Galactica', 'Handbook', 'Great Galloping', 'Entry Cards',
                        'Galactic Era', 'War', 'Navigation', 'Fearless', 'University Library', 'High Priest',
                        'Kalgan Central', 'Dokor', 'Lathan', 'June', 'Lens', 'City Hall', 'States', 'Grand', 'Tyrant',
                        'Rossem-', 'Indbur III', 'News', 'First Citizen', 'Hart', 'Opening', 'Automatic Super', 'State',
                        'Prophet', 'Ankor Jael', 'Rift', 'Satisfied Turbor', 'Hmph', 'Radiant Fields', 'Galaxywide',
                        'Terel', 'Main Fleet', 'Crown', 'Levi Norast', 'Pelleas Author', 'Super', 'Far',
                        'Ambassador Verisof', 'Leftish', 'Square', 'Anc/', 'Black', 'Seldon Crisis', 'Dark Nebula',
                        'Pelot', 'Chief Engineer', 'Korillov', 'Pluema', 'Sergeant Demen', 'Glory', 'Commander',
                        'Committee', 'Locris', 'Tamper Plateaus', 'Prince', 'City Council', 'Late Empire', 'Ankor',
                        'Squire', 'Golly', 'Home', 'Old Days', 'Foundationers', 'Judge', 'Emotional', 'Detectors',
                        'Race', 'Rusty', 'Trusts', 'Great Hall', 'Y\'know', 'Imperial Splendor', 'Barons', 'Loris',
                        'Galactic Empire', 'GALACTICA.There', 'Summa', 'Bull Trader', 'Stoop', 'Encyclopedia Building',
                        'Normannic', 'Unkeyed', 'Fiari', 'ol\' Foundation', 'Orum Palley', 'Prime', 'Foundational Era',
                        'Shhh', 'First Class', 'Bureau', 'East', 'Lo Moro', 'Sef Sermak', 'Unkeyed Memories',
                        'Locris University', 'Viceregal Palace', 'Communi', 'Cellomet', 'Outlanders', 'Toran Darell',
                        'Limmar Ponyets', 'Mori Luk', 'Huxlani', 'west Trantor', 'Ill', 'Drift', 'Trade',
                        'Nuclear Field', 'Automatic', 'Historical Museum', 'Glyptal IV', 'Action Party', 'Dryly',
                        'Mnemon', 'Nonsense', 'PRINCES i.', 'Licia', 'Trustees', 'smiled Darell', 'Federation',
                        'Massacre', 'Flas', 'Foreign', 'Ducem', 'Encyclopedists', 'Psychic', 'Seven Days',
                        'Underground Party', 'Primate', 'War QUORISTON', 'Whereupon', 'Channel', 'Galaxy f',
                        'Galactic Field', 'Gamma', 'Seldon Plan', 'Splendor', 'Unconverted', 'Satisfied',
                        'Seldon Convention', 'Yume', 'Field Bearings', 'Dagobert X', 'Plan-', 'Mutant', 'Offhand',
                        'Paramay', 'Central Theater', 'Centauwi', 'Lewis Pirenne', 'Whassallian Rift', 'Blue',
                        'Cyclopedia', 'Imperial Sector', 'Reception Indicator', 'Gleiar', 'Young', 'Offices',
                        'Opposition', 'Historical', 'Junior Officer', 'Grand Detectors', 'Imperial', 'Gleiar City',
                        'Research', 'Eden', 'Lewis Bort', 'Jan', 'Orsha II', 'Prime Radiant', 'Qualified',
                        'Council Chambers', 'Station', 'Snake Sutt', 'Noble Lords', 'Daluben IV', 'Mommuh',
                        'Pax Imperium', 'Jord Fara', 'Sergeant Mori', 'Alpha', 'Holy Planet', 'Eardrum', 'Mission',
                        'Intelligence', 'Priest', 'Routine', 'Lev Meirus', 'Commander Cenn', 'Unless-', 'Energy',
                        'Randel', 'Central Hall', 'Four Kingdoms', 'Arid', 'Arcadia Darell', 'Porfirat Hart',
                        'Warlords', 'Foundationism', 'Fought', 'Encyclopedia Committee', 'Humanity', 'Trantorians',
                        'Demanding-', 'Mountel', 'Great Space', 'Bull', 'Commissioner Linge', 'Seven', 'Protector',
                        'Capital', 'Ifni', 'Pause', 'Tribune', 'Hall', 'Nuts', 'Anacreon navy', 'Dam', 'Konom',
                        'Secret', 'Time', 'Foreign Secretary', 'Third Interlude', 'Independents', 'Temporary',
                        'Memories', 'Officer Tippellum', 'Isaac', 'Identification', 'Galactic Lens', 'Class', 'Princes',
                        'Lyonesse', 'Psychohistorian', 'Governor', 'Les', 'Twuly', 'Lepold I', 'Columbia University',
                        'Milky Way', 'Forces', 'Nova', 'Executive', 'Molff Resonator', 'Electromathematics',
                        'Independent Trading', 'Blind', 'Privy', 'Molff', 'Encyclopedia Foundation', 'Record', 'Owigin',
                        'Brooklyn', 'Delight', 'Sire', 'Grand Detector', 'Space Route', 'Hokum', 'Helicon', 'Olynthus',
                        'Chief Commissioner', 'Ship', 'Bandy', 'Vega', 'Ovall Gri', 'Democratic Opposition', 'Answer',
                        'Great Sack', 'psychohistorian Seldon', 'Lordship', 'Bearings', 'Control', 'Sea', 'Added Sutt',
                        'Project', 'Squire Jord', 'Luk', 'Disinto', 'Vegan', 'Ebling', 'Visi', 'Unless', 'Standard Day',
                        'Autarchy', 'Conversion', 'Heaven', 'World', 'Seldon Project', 'Second Interlude', 'Ptah',
                        'Setdon', 'Flere', 'Lors', 'Unimara', 'Great', 'Patrician Barr', 'Pewiphewy', 'Spiritual',
                        'Twentieth Fleet', 'Personal', 'Rebellion', 'Admiral', 'Depressor', 'Entry', 'Trantorian',
                        'Pleiades', 'Division', 'First Citizenship', 'questioned Toran', 'Bier', 'Smite', 'Independent']

    return people_list, location_list, unclassified


def ner_person(doc, token):
    """
    :return: True if @token has person behaviour
    """
    if token.dep_ == "nsubj" and token.head.pos_ == 'VERB' and token.head.lemma_ in person_verbs:
        return True
    else:
        for i, word in enumerate(doc):
            if str(word) in honorific_words and i < len(doc) - 1 and doc[i + 1] == token:
                return True
    return False


def ner_location(doc, token):
    """
    1 - if sentence has PERSON, and within its coreferences in the sentence there is a location_noun e.g. 'planet'
    2 - if the sentence is of the form "VERB + to + PERSON" -> Person is a candidate of location
    :return: True if @token has location behaviour
    """
    matcher.add('location', [location_name_pattern])
    m = matcher(doc)
    for match_id, start, end in m:
        span = doc[start: end]
        for word in location_name:
            if word in str(span) and str(token) in str(span):
                return True

    matcher.add('location', [travel_to_pattern])
    m = matcher(doc)
    for match_id, start, end in m:
        span = doc[start: end]
        if len([x for x in nlp(str(span)) if x.pos_ == "VERB" and str(x.lemma_) in travel_to_verbs]) and str(
                token) in str(span):
            return True


def ner_event(doc):
    """
    Fact analyses
    Most events are build around patterns of the form: <OBJECT> <VERB> <SUBJECT>
    #TODO: see course 5 slide 35
    """
    subject = ""
    direct_object = ""
    indirect_object = ""
    verb = ""
    # get token dependencies
    for word in doc:
        # subject would be
        if word.dep_ == "nsubj":
            subject = word.orth_
        # iobj for indirect object
        elif word.dep_ == "iobj":
            indirect_object = word.orth_
        # dobj for direct object
        elif word.dep_ == "dobj":
            direct_object = word.orth_
        elif word.dep_ == 'ROOT':
            verb = word
    if str(subject) != "" and str(verb) != "" and str(direct_object) != "":
        print("----------Event---------\n - '", doc.text, "'\n - Who? ", subject, "\n - What?: ", verb, "\n - vs Who? ",
              direct_object, "\n - indirect object: ", indirect_object)
