"""
Location-person links
https://plotly.com/python/images/#add-a-background-image
https://plotly.com/python/line-and-scatter/
https://plotly.com/python/reference/#scatter-texttemplate
https://plotly.com/python/text-and-annotations/
"""
from utils import read_list
import plotly.graph_objects as go

GALAXY = [[425, 400, "Rossem"],
          [1100, 700, "Haven"],
          [770, 490, "Neotrantor"],
          [1300, 600, "Askone"],
          [500, 500, "Tazenda"],
          [430, 200, "Arcturus"],
          [170, 610, "Kalgan"],
          [160, 650, "Terminus"],
          [210, 690, "Anacreon"],
          [1200, 680, "Synnax"],
          [900, 650, "Radole"],
          [700, 500, "Trantor"]]
planet_names = [x[2] for x in GALAXY]
planets_x = [x[0] for x in GALAXY]
planets_y = [x[1] for x in GALAXY]
test = ["Tests<br>"+str(i) for i in range(12)]

location_links = read_list("location_links")
hover = [[] for x in range(len(planet_names))]
for link in location_links:
    person = link[1]
    idx = [i for i, x in enumerate(planet_names) if x == link[0]]
    if any(idx):
        hover[idx[0]].append(person)

PEOPLE = ["<b>Linked PER entities:<b><br>- " + "<br>- ".join(y) for y in [list(set(x)) for x in hover]]

# Create figure
fig = go.Figure()

# region Image with Zoom

image_url = "https://images.pexels.com/photos/2312040/pexels-photo-2312040.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
# Constants
img_width = 6000
img_height = 4000
scale_factor = 0.25

# Add invisible scatter trace.
# This trace is added to help the autoresize logic work.
fig.add_trace(
    go.Scatter(
        x=[0, img_width * scale_factor],
        y=[0, img_height * scale_factor],
        mode="markers",
        marker_opacity=0
    )
)

# Configure axes
fig.update_xaxes(
    visible=False,
    range=[0, img_width * scale_factor]
)

fig.update_yaxes(
    visible=False,
    range=[0, img_height * scale_factor],
    # the scaleanchor attribute ensures that the aspect ratio stays constant
    scaleanchor="x"
)

# Add image
fig.add_layout_image(
    dict(
        x=0,
        sizex=img_width * scale_factor,
        y=img_height * scale_factor,
        sizey=img_height * scale_factor,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="below",
        sizing="stretch",
        source="https://images.pexels.com/photos/2312040/pexels-photo-2312040.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940")
)

# Configure other layout
fig.update_layout(
    title_text="Foundation Trilogy Galaxy",
    width=img_width * scale_factor,
    height=img_height * scale_factor,
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
    legend=dict(
        # Adjust click behavior
        itemclick="toggleothers",
        itemdoubleclick="toggle",
    )
)
# endregion

fig.add_trace(go.Scatter(
    name="Planet",
    x=planets_x,
    y=planets_y,
    opacity=0.8,
    mode="markers+text",
    text=planet_names,
    textposition="top center",
    hovertext=PEOPLE,
    showlegend=False,
    marker=dict(
            color='White',
            size=10),
    textfont=dict(
        size=14,
        color="White",
    )
))
fig.show(config={'displayModeBar': False, "showTips": False, 'displaylogo': False})
fig.write_html("renders/EntityGeoMapping.html")
