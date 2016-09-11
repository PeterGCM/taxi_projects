import __init__
#
from community_analysis import com_summary_fpath
#
from taxi_common.file_handling_functions import check_path_exist
#
import folium
from plotly.graph_objs import *


def com_stats_summary():
    if not check_path_exist(com_summary_fpath):

        return
    else:
        pass



def draw_grid_on_map(map_osm, x_points, y_points):
    # horizontal lines
    for x in x_points:
        sx, sy, ex, ey = x, y_points[0], x, y_points[-1]
        map_osm.add_children(folium.PolyLine(locations=[(sy, sx), (ey, ex)], weight=0.5))
    # vertical lines
    for y in y_points:
        sx, sy, ex, ey = x_points[0], y, x_points[-1], y
        map_osm.add_children(folium.PolyLine(locations=[(sy, sx), (ey, ex)], weight=0.5))
    return map_osm


def generate_3D_graph(labels, group, layt, Edges):

    N = len(labels)

    Xn = [layt[k][0] for k in range(N)]
    Yn = [layt[k][1] for k in range(N)]
    Zn = [layt[k][2] for k in range(N)]

    Xe = []
    Ye = []
    Ze = []
    for e in Edges:
        Xe += [layt[e[0]][0], layt[e[1]][0], None]
        Ye += [layt[e[0]][1], layt[e[1]][1], None]
        Ze += [layt[e[0]][2], layt[e[1]][2], None]



    trace1 = Scatter3d(x = Xe, y = Ye, z = Ze,
                       mode = 'lines',
                       line=Line(color='rgb(125,125,125)', width = 1),
                       hoverinfo = 'none'
                      )
    trace2 = Scatter3d(x = Xn, y = Yn, z = Zn,
                       mode = 'markers',
                       name = 'actors',
                       marker = Marker(symbol = 'dot',
                                       size = 6,
                                       color = group,
                                       colorscale = 'Viridis',
                                       line = Line(color = 'rgb(50,50,50)', width = 0.5)
                                      ),
                       text=labels,
                       hoverinfo = 'text'
                       )
    axis = dict(showbackground = False,
               showline = False,
               zeroline = False,
               showgrid = False,
               showticklabels = False,
               title = ''
               )
    layout = Layout(
             title="Network of taxi full time drivers",
             width=1000,
             height=1000,
             showlegend=False,
             scene=Scene(
             xaxis=XAxis(axis),
             yaxis=YAxis(axis),
             zaxis=ZAxis(axis),
            ),
         margin=Margin(
            t=100
        ),
        hovermode='closest',
        annotations=Annotations([
               Annotation(
               showarrow=False,
                text="Data source: comfort",
                xref='paper',
                yref='paper',
                x=0,
                y=0.1,
                xanchor='left',
                yanchor='bottom',
                font=Font(
                size=14
                )
                )
            ]),    )

    data = Data([trace1, trace2])
    fig = Figure(data=data, layout=layout)
    return fig
