import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime

OPENSKY_API = "https://opensky-network.org/api/states/all"

def fetch_data(bbox=None):
    try:
        params = bbox if bbox else {}
        response = requests.get(OPENSKY_API, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return None

def states_to_df(data):
    cols = [
        'icao24','callsign','origin_country','time_position','last_contact',
        'longitude','latitude','baro_altitude','on_ground','velocity',
        'true_track','vertical_rate','sensors','geo_altitude',
        'squawk','spi','position_source'
    ]
    
    states = data.get('states') or []
    filtered_states = [s for s in states if len(s) == len(cols)]
    
    df = pd.DataFrame(filtered_states, columns=cols)
    df['callsign'] = df['callsign'].fillna('').str.strip()
    df = df.fillna({
        'geo_altitude': 0, 
        'baro_altitude': 0, 
        'velocity': 0, 
        'latitude': 0, 
        'longitude': 0
    })
    return df

def make_map(df):
    m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=6)
    for _, row in df.iterrows():
        if row['latitude'] and row['longitude']:
            popup = f"{row['callsign']}<br>{row['origin_country']}<br>Alt: {int(row['geo_altitude'])}m"
            color = "green" if not row['on_ground'] else "red"
            folium.CircleMarker(
                location=(row['latitude'], row['longitude']),
                radius=4,
                popup=popup,
                color=color,
                fill=True
            ).add_to(m)
    return m

def main():
    st.set_page_config(page_title="Live Flight Tracker", layout="wide")
    st.title("Real-Time Flight Tracker (North Germany Area)")
    st.markdown("Live data from [OpenSky Network](https://opensky-network.org/)")

    with st.sidebar:
        st.header("Custom Region")
        lamin = st.number_input("Min Latitude", value=50.0, step=0.1)
        lamax = st.number_input("Max Latitude", value=55.0, step=0.1)
        lomin = st.number_input("Min Longitude", value=5.0, step=0.1)
        lomax = st.number_input("Max Longitude", value=15.0, step=0.1)
        refresh = st.button("Refresh Data")

    bbox = {"lamin": lamin, "lomin": lomin, "lamax": lamax, "lomax": lomax}
    data = fetch_data(bbox)

    if not data:
        st.stop()

    ts = datetime.utcfromtimestamp(data["time"]).strftime('%Y-%m-%d %H:%M:%S UTC')
    df = states_to_df(data)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Aircraft", len(df))
    col2.metric("On Ground", int(df['on_ground'].sum()))
    col3.metric("In Air", len(df) - int(df['on_ground'].sum()))
    col4.metric("Avg Altitude (m)", f"{df['geo_altitude'].mean():.1f}")

    st.subheader(f"Aircraft Data Table — {ts}")
    st.dataframe(df[['callsign', 'origin_country', 'latitude', 'longitude', 'geo_altitude', 'velocity']])

    st.subheader("Aircraft Positions Map")
    folium_static(make_map(df))

if __name__ == "__main__":
    main()
