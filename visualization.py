from utils import *
from pandas import DataFrame
import networkx
import matplotlib.pyplot as plt
from pyvis.network import Network
from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8
from bokeh.transform import linear_cmap
from networkx.algorithms import community

test = [('Mule', 'Seldon'), ('Test', 'Mule')]


def preprocess_tuple(tuple_list):
    new_list = []
    for connection in tuple_list:
        new_tuple = []
        for i, entity in enumerate(connection):
            if i != 2:
                if len(entity) > 1:
                    new_tuple.append(entity[1])
                else:
                    new_tuple.append(entity[0])
        new_list.append((new_tuple[0], new_tuple[1], connection[2]))
    return new_list


def network_graph(tuple_list):
    tuple_list = preprocess_tuple(tuple_list)
    df = DataFrame(tuple_list, columns=['Source', 'Target', 'weights'])
    G = nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='weights')
    net = Network(notebook=True)
    net.from_nx(G)
    net.show("entity_network_graph.html")


def super_network(tuple_list):
    """
    https://melaniewalsh.github.io/Intro-Cultural-Analytics/Network-Analysis/Making-Network-Viz-with-Bokeh.html
    """

    tuple_list = preprocess_tuple(tuple_list)
    df = DataFrame(tuple_list, columns=['Source', 'Target', 'Weight'])
    G = networkx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')

    # Calculate degree for each node and add as node attribute
    degrees = dict(networkx.degree(G))
    networkx.set_node_attributes(G, name='degree', values=degrees)

    number_to_adjust_by = 5
    adjusted_node_size = dict([(node, degree + number_to_adjust_by) for node, degree in networkx.degree(G)])
    networkx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)

    # Choose attributes from G network to size and color by — setting manual size (e.g. 10) or color (e.g. 'skyblue') also allowed
    size_by_this_attribute = 'adjusted_node_size'
    color_by_this_attribute = 'adjusted_node_size'

    # Pick a color palette — Blues8, Reds8, Purples8, Oranges8, Viridis8
    color_palette = Blues8

    # Choose a title!
    title = 'Foundation Trilogy Network'

    # Establish which categories will appear when hovering over each node
    # Establish which categories will appear when hovering over each node
    HOVER_TOOLTIPS = [
        ("Character", "@index"),
        ("Degree", "@degree")
    ]

    # Create a plot — set dimensions, toolbar, and title
    plot = figure(tooltips=HOVER_TOOLTIPS,
                  tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
                  x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

    # Create a network graph object
    # https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html\
    network_graph = from_networkx(G, networkx.spring_layout, scale=10, center=(0, 0))

    # Set node sizes and colors according to node degree (color as spectrum of color palette)
    minimum_value_color = min(network_graph.node_renderer.data_source.data[color_by_this_attribute])
    maximum_value_color = max(network_graph.node_renderer.data_source.data[color_by_this_attribute])
    network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute,
                                               fill_color=linear_cmap(color_by_this_attribute, color_palette,
                                                                      minimum_value_color, maximum_value_color))

    # Set edge opacity and width
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

    plot.renderers.append(network_graph)

    show(plot)
    # save(plot, filename=f"{title}.html")


super_network(links_list)
