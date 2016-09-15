import __init__
#
from community_analysis import com_summary_2009_fpath
#
from taxi_common.file_handling_functions import check_path_exist, save_pickle_file, get_all_directories, get_all_files
#
from plotly.graph_objs import *
import pandas as pd
import folium

def get_com_stats_summary():
    if not check_path_exist(com_summary_2009_fpath):
        from community_analysis import com_dir
        headers = ['Threshold value (Day)', 'Num of community', 'Num of drivers',
                   'Average', 'Median', 'SD', 'Skewness', 'Kurtosis',
                   'List of communities, (community ID, # of drivers)']
        df_data = {k: [] for k in headers}
        L_THD, L_NC, L_ND, L_A, L_M, L_SD, L_SK, L_KU, L_LC = range(len(headers))

        #
        for dn in get_all_directories(com_dir):
            dpath = '%s/%s' % (com_dir, dn)
            summary_fn = get_all_files(dpath, '', '.csv').pop()
            _, _, str_thD, _, _ = summary_fn[:-len('.csv')].split('-')
            thD = int(str_thD[len('thD('):-len(')')])
            df = pd.read_csv('%s/%s' % (dpath, summary_fn))
            df_data[headers[L_THD]].append(thD)
            df_data[headers[L_NC]].append(df['num-nodes'].count())
            df_data[headers[L_ND]].append(df['num-nodes'].sum())
            df_data[headers[L_A]].append(df['num-nodes'].mean())
            df_data[headers[L_M]].append(df['num-nodes'].median())
            df_data[headers[L_SD]].append(df['num-nodes'].std())
            df_data[headers[L_SK]].append(df['num-nodes'].skew())
            df_data[headers[L_KU]].append(df['num-nodes'].kurt())
            df_data[headers[L_LC]].append(','.join(['{%s:%d}' % (cname, num_nodes)
                                                for cname, num_nodes in df.loc[:, ['com-name', 'num-nodes']].values]))
        df = pd.DataFrame(df_data)[headers]
        df.to_csv(com_summary_2009_fpath, index=False)
        return df
    else:
        return pd.read_csv(com_summary_2009_fpath)


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

if __name__ == '__main__':
    print get_com_stats_summary()