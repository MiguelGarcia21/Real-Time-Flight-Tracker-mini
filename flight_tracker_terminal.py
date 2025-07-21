import requests
import pandas as pd
import time
from datetime import datetime
import folium

OPENSKY_URL = "https://opensky-network.org/api/states/all"

# this is for berlin area
BBOX = {
    'lamin': 52.2,
    'lomin': 13.0,
    'lamax': 52.7,
    'lomax': 13.8
}

def fetch_states(bbox=None, username=None, password=None):
    params = bbox if bbox else {}
    auth = (username, password) if username and password else None
    r = requests.get(OPENSKY_URL, params=params, auth=auth)
    r.raise_for_status()
    return r.json()

def states_to_df(data):
    cols = [
        'icao24', 'callsign', 'origin_country', 'time_position', 'last_contact',
        'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity',
        'true_track', 'vertical_rate', 'sensors', 'geo_altitude',
        'squawk', 'spi', 'position_source'
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

def analyze_df(df):
    return {
        'total_planes': len(df),
        'on_ground': int(df['on_ground'].sum()),
        'in_air': len(df) - int(df['on_ground'].sum()),
        'avg_altitude_m': df['geo_altitude'].mean()
    }

def make_map(df, filename="current_map.html"):
    m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=7)
    for _, row in df.iterrows():
        if row['latitude'] and row['longitude']:
            popup = f"{row['callsign']} {int(row['geo_altitude'])}m"
            color = 'green' if not row['on_ground'] else 'red'
            folium.CircleMarker(
                location=(row['latitude'], row['longitude']),
                radius=4,
                popup=popup,
                color=color,
                fill=True
            ).add_to(m)
    m.save(filename)

def main(pause=30):
    print("Fetching real-time flight data from OpenSky...\n")
    while True:
        try:
            data = fetch_states(bbox=BBOX)
            df = states_to_df(data)
            summary = analyze_df(df)
            ts = datetime.utcfromtimestamp(data['time']).strftime('%Y-%m-%d %H:%M:%S UTC')
            print(f"[{ts}] Total: {summary['total_planes']} | In Air: {summary['in_air']} | On Ground: {summary['on_ground']} | Avg Alt: {summary['avg_altitude_m']:.1f}m")
        except Exception as e:
            print("Error:", e)
        time.sleep(pause)

if __name__ == "__main__":
    main()
