# Python Imports
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Environment Variables
DATAFRAME = pd.core.frame.DataFrame

def read_excel(filename):
    return pd.read_excel(filename, header=0, index_col=0)


def check_dataframe(data):
    if type(data) == pd.core.frame.DataFrame:
        return all(x in data.columns for x in ['Lat', 'Lon'])
    else:
        False


def drop_latlon_rows(data, action, drop_index=None):
    if action == "check":
        lat_zero = data['Lat'] == 0
        lon_zero = data['Lon'] == 0
        return list(data[lat_zero & lon_zero].index)

    elif action == "drop":
        data.drop(drop_index, axis = 0, inplace=True)
        return data.reset_index(drop=True, inplace=True)


def plot_map(df, datatype, marker_location=-1):
    fig = px.scatter_mapbox(df,
                        lat="Lat", lon="Lon",
                        hover_name="DateTime",
                        hover_data=["{}".format(datatype)],
                        color=datatype,
                        color_continuous_scale=px.colors.sequential.thermal,
                        center= dict(lat=df.loc[0, "Lat"], lon=df.loc[0, "Lon"]),
                        zoom=13, height=300)
    
    fig.add_trace(px.scatter_mapbox(df.iloc[[marker_location]],
                                    lat="Lat", lon="Lon",
                                    hover_name="DateTime",
                                    color=datatype,
                                    opacity=1,
                                    size=pd.Series([0.001]),
                                    ).data[0])

    fig.update_layout(mapbox_style="open-street-map",
                      margin={"r":0,"t":0,"l":45,"b":0})

    return fig



def plot_line(df, datatype, marker_location=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["DateTime"], y=df[datatype],
                                mode="lines+markers",
                                name=datatype,
                                text=df.index))
    if marker_location != -1:
        fig.add_annotation(
                x=df.iloc[marker_location]["DateTime"],
                y=df.iloc[marker_location][datatype],
                text="{} = {} {}".format(datatype, df.iloc[marker_location][datatype], df.iloc[marker_location]["DateTime"]))
        fig.update_annotations(dict(
                xref="x",
                yref="y",
                showarrow=True,
                font=dict(
                    family="Courier New, monospace",
                    size=8,
                    color="#ffffff"),
                align="center",
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#636363",
                ax=20,
                ay=-40,
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8
            ))


    fig.update_layout(xaxis_title="TimeStamp",
                      yaxis_title=datatype,
                      width=700,
                      height=300,

                      margin={"r":80,"t":0,"l":0,"b":0})

    return fig




def plot_all_line(df, typ_list=None):
    meta_data = {"PM":
                    {
                        "values": ["PM1", "PM2.5", "PM10"],
                        "text"  : "WhiteBurn Test - PM values",
                        "yaxis" : "PM [ug/m3]",
                        "yrange": [0, 500]
                    },
                "Temperature":
                    {
                        "values": ["Temperature"],
                        "text"  : "WhiteBurn Test - Temperature values",
                        "yaxis" : "Temperature [C]",
                        "yrange": [0, 40]
                    },
                "Humidity":
                    {
                        "values": ["Humidity"],
                        "text"  : "WhiteBurn Test - Humidity values",
                        "yaxis" : "Humidity [%]",
                        "yrange": [0, 100]
                    },
                "FlowRate":
                    {
                        "values": ["FlowRate"],
                        "text"  : "WhiteBurn Test - Flow Rate values",
                        "yaxis" : "Flow Rate [L/sec]",
                        "yrange": [0, 700]
                    },
                "Noise":
                    {
                        "values": ["Noise"],
                        "text"  : "WhiteBurn Test - Noise values",
                        "yaxis" : "Noise [0-4026]",
                        "yrange": [0, 1000]
                    },
                "Acc":
                    {
                        "values": ["AccX", "AccY", "AccZ"],
                        "text"  : "WhiteBurn Test - Acceleration values",
                        "yaxis" : "Acc [g]",
                        "yrange": [-6000, 6000]
                    },
                }


    fig = make_subplots(rows = len(typ_list), cols = 1,
                        shared_xaxes=True,
                        vertical_spacing=0.05,
                        subplot_titles= [meta_data[typ]["text"] for typ in typ_list])


    for itr in range(len(typ_list)):
        for col in meta_data[typ_list[itr]]["values"]:
            fig.add_trace(go.Scatter(x=df["DateTime"], y=df[col],
                            mode="lines+markers",
                            name=col),
                            row=itr+1, col=1)

            fig.update_yaxes(title_text=meta_data[typ_list[itr]]["yaxis"],
                             range=meta_data[typ_list[itr]]["yrange"],
                             row=itr+1, col=1)

        fig.update_traces(xaxis="x1")
        fig.update_xaxes(spikemode='across+marker')

        fig.update_layout(
            height=1000,
            font=dict(
                family="Courier New, monospace",
                size=10,
                color="#7f7f7f"))

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig





if __name__ == "__main__":

    # Filepath
    path = "Compiled_SenData.xlsx"
    # Read excel
    data = read_excel(path)
    # Check dataframe
    if check_dataframe(data):
        index_to_drop = drop_latlon_rows(data, action="check")
        drop_latlon_rows(data, action="drop", drop_index=index_to_drop)

