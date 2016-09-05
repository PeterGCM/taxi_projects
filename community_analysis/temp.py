from plotly.graph_objs import *


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
