# Real-Time-Flight-Tracker-mini

A Python application that visualizes live aircraft positions using OpenSky Network API data. This mini-project includes both a Streamlit web interface and a terminal version.

## Features 
- **Real-time aircraft tracking** with 30-second updates
- **Interactive map** showing plane positions and status
- **Data metrics** - total aircraft, in-air/ground status, altitude
- **Customizable region** selection
- **Dual interfaces**: 
  - Web GUI (Streamlit)
  - Terminal version
- Aircraft details: callsign, origin country, position, altitude, velocity

## Requirements 
- Python 3.8+
- Streamlit
- Pandas
- Folium
- Requests
- Streamlit-folium

## Installation 
1. Clone the repository:
```bash
git clone https://github.com/MiguelGarcia21/Real-Time-Flight-Tracker-mini.git
cd flight-tracker
```

2. Install dependencies:
```bash
pip install streamlit folium streamlit-folium pandas requests
```

## Usage

### Web GUI Version
```bash
streamlit run flight_tracker_gui.py
```

1. Adjust region coordinates in sidebar (default: North Germany/Netherlands)
2. Click "Refresh Data" to update
3. View aircraft on interactive map
4. Examine detailed data in table

### Terminal Version
```bash
python flight_tracker_terminal.py
```

- Runs continuously with 30-second updates
- Displays aircraft counts and average altitude

## Configuration
Customize default regions in code, or the left slidebar within the GUI:
```python
# GUI version (flight_tracker_gui.py)
lamin = st.number_input("Min Latitude", value=50.0)
lamax = st.number_input("Max Latitude", value=55.0)
lomin = st.number_input("Min Longitude", value=5.0)
lomax = st.number_input("Max Longitude", value=15.0)

# Terminal version (flight_tracker_terminal.py)
BBOX = {
    'lamin': 52.2,  # Berlin area
    'lomin': 13.0,
    'lamax': 52.7,
    'lomax': 13.8
}
```

## Quick Notes
- Uses [OpenSky Network REST API](https://openskynetwork.github.io/opensky-api/)
- Data updated every 10-15 seconds
- Map shows:
  - Green markers = airborne
  - Red markers = on ground
