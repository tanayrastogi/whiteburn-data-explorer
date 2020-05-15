# Python Imports
import streamlit as st 
from datetime import datetime

# Local import
import utils as ut

# Environment Variable
DATE = "2020-05-14"
TITLE = "Whiteburn Data Analysis"


def data_uploader():
    # Uploading data
    uploaded_file = st.file_uploader("Upload the Sensor Data file (only .XLSX format)", type="xlsx")
    if uploaded_file is not None:
        return ut.read_excel(uploaded_file)
    else:
        return None

def check_latlon(data):
    # Check if there are any rows with lat/lon zero
    no_of_rows_dropped = ut.drop_latlon_rows(data, action="check")
    if len(no_of_rows_dropped) > 0:
        st.write("Droping index for with no value of lat/lon: {} ".format(no_of_rows_dropped))
        ut.drop_latlon_rows(data, action="drop", drop_index=no_of_rows_dropped)
        st.write("Resultant dataframe: ", data.shape)

def show_data(data):
    st.dataframe(data)


def data_on_map():
    # Side bar
    selection_list = ["PM1", "PM2.5", "PM10", "FlowRate", "Temperature", "Humidity", "Noise", "AccX", "AccY", "AccZ"]
    st.sidebar.title("Select data type to show on map")
    return st.sidebar.selectbox("Data Types", selection_list)


def plot_map(data, datatype):
    st.header("Map")
    index = st.slider("Select Timestamp",
                                 min_value = int(-1),
                                 max_value = int(data.index[-1]),
                                 step=int(1),
                                 value=int(-1))

    if index > -1:
        st.write("Time Stamp: {}".format( data.loc[index, "DateTime"].strftime("%m/%d/%Y, %H:%M:%S")  ))
    fig_map = ut.plot_map(data, datatype, marker_location=index)
    fig_lin = ut.plot_line(data, datatype, marker_location=index) 
    st.plotly_chart(fig_map)
    st.plotly_chart(fig_lin)


def plot_all_line(data):
    st.header("Plotting All Data")
    types = ["Temperature", "PM", "Humidity", "FlowRate", "Noise", "Acc"]

    # Checkboxex
    plot_types = list()
    st.write("Select data type to plot")
    for t in types:
        if st.checkbox(t):
            plot_types.append(t)
    if len(plot_types) > 0:
        fig = ut.plot_all_line(data, plot_types)
        st.plotly_chart(fig)



def main():
    # Title
    st.title(TITLE)

    # Upload Data
    data = data_uploader()

    # If data is read
    if ut.check_dataframe(data):
        # Check if there are any rows with lat/lon zero
        check_latlon(data)

        # Checkbox for showing data
        if st.checkbox("Show Dataframe"):
            show_data(data)

        # Map
        # Select data type to plot
        datatype = data_on_map()
        plot_map(data, datatype)

        # Plot All
        plot_all_line(data)






    else:
        st.error("Either no file uploded or the file does not have 'Lat'/'Lon' column")



if __name__ =="__main__":
    main()