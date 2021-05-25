from pandas import DataFrame
import networkx
from bokeh.io import show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine, NodesAndLinkedEdges, LabelSet
from bokeh.plotting import figure, from_networkx
from bokeh.palettes import Blues8, Spectral11
from networkx.algorithms import community as commun
from normalization import normalize_list
from utils import read_list


def preprocess_tuple(tuple_list):
    new_list = []
    for connection in tuple_list:
        new_list.append((str(connection[0]), str(connection[1]), connection[2]))
    return new_list


def CHARACTER_NETWORK():
    """
    https://melaniewalsh.github.io/Intro-Cultural-Analytics/Network-Analysis/Making-Network-Viz-with-Bokeh.html
    """
    tuple_list = normalize_list(read_list("people_links"))
    [tuple_list.remove(x) for x in tuple_list if "Galaxy" in x]
    tuple_list = preprocess_tuple(tuple_list)
    df = DataFrame(tuple_list, columns=['Source', 'Target', 'Weight'])
    G = networkx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')

    # Calculate communities
    communities = commun.greedy_modularity_communities(G)
    # Create empty dictionaries
    modularity_class = {}
    modularity_color = {}
    modularity_color2 = {}
    # Loop through each community in the network
    for community_number, community in enumerate(communities):
        # For each member of the community, add their community number and a distinct color
        for name in community:
            modularity_class[name] = community_number
            modularity_color[name] = Spectral11[community_number]

    # Add modularity class and color as attributes from the network above
    networkx.set_node_attributes(G, modularity_class, 'modularity_class')
    networkx.set_node_attributes(G, modularity_color, 'modularity_color')

    # Calculate degree for each node and add as node attribute
    degrees = dict(networkx.degree(G))
    networkx.set_node_attributes(G, name='degree', values=degrees)

    number_to_adjust_by = 5
    adjusted_node_size = dict([(node, degree + number_to_adjust_by) for node, degree in networkx.degree(G)])
    networkx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)

    # Choose colors for node and edge highlighting
    node_highlight_color = 'white'
    edge_highlight_color = 'black'

    # Choose attributes from G network to size and color by — setting manual size (e.g. 10) or color (e.g. 'skyblue') also allowed
    size_by_this_attribute = 'adjusted_node_size'
    color_by_this_attribute = 'modularity_color'

    # Pick a color palette — Blues8, Reds8, Purples8, Oranges8, Viridis8
    color_palette = Blues8

    # Choose a title!
    title = 'The Foundation Trilogy Network'

    # Establish which categories will appear when hovering over each node
    HOVER_TOOLTIPS = [
        ("Character", "@index"),
        ("Degree", "@degree"),
        ("Modularity Class", "@modularity_class"),
        ("Modularity Color", "$color[swatch]:modularity_color"),
    ]

    # Create a plot — set dimensions, toolbar, and title
    plot = figure(tooltips=HOVER_TOOLTIPS,
                  tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
                  x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title, height=800, width=1500)
    plot.axis.visible = False

    # Create a network graph object
    # https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
    network_graph = from_networkx(G, networkx.spring_layout, scale=10, center=(0, 0))

    # Set node sizes and colors according to node degree (color as category from attribute)
    network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=color_by_this_attribute)
    # Set node highlight colors
    network_graph.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color,
                                                     line_width=2)
    network_graph.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color,
                                                         line_width=2)

    # Set edge opacity and width
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)
    # Set edge highlight colors
    network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
    network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)

    # Highlight nodes and edges
    network_graph.selection_policy = NodesAndLinkedEdges()
    network_graph.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(network_graph)

    # Add Labels
    x, y = zip(*network_graph.layout_provider.graph_layout.values())
    node_labels = list(G.nodes())
    source = ColumnDataSource({'x': x, 'y': y, 'name': [node_labels[i] for i in range(len(x))]})
    labels = LabelSet(x='x', y='y', text='name', source=source, background_fill_color='white', text_font_size='10px',
                      background_fill_alpha=.7)
    plot.renderers.append(labels)

    show(plot)
    #save(plot, filename=f"{title}.html")


if __name__ == '__main__':
    CHARACTER_NETWORK()
