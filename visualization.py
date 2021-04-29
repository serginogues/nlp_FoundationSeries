from pandas import DataFrame
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

test = [('Mule', 'Seldon', 3), ('Bayta', 'Mule', 25)]
df = DataFrame(test, columns=['Source', 'Target', 'weights'])
G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='weights')
net = Network(notebook=True)
net.from_nx(G)
net.show("example.html")
