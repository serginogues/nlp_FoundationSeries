"""
Report in research paper format
Sections:
    - Abstract
    - Introduction
    - Background (related work)
    - Approach
    - Dataset (book + Validation points)
    - Algorithms
    - Experiments
    - Future research
    - References
Add as well in the report what doubts we have and what is not clear
"""

from entity_identification import *

if __name__ == '__main__':

    parsed_list = preprocess(FoundationTrilogy)
    people_list, people_list_df = entity_identification(parsed_list)
    #ToDo:
    # - https://www.snorkel.org/use-cases/spouse-demo
    # - negation handling, co-reference & pronoun handling and normalization of entities before visualization.
    # - measure the quality
    # - One or more visualizations. Word Cloud does not count as a visualization!
    # - Detecting anomalies gets you bonus points
    # - Creating a great video with audio also gets you bonus points
