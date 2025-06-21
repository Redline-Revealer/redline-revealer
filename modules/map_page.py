"""Redlining Map Page for Redline Revealer.

Displays interactive overlays of historical redlining and housing risk.
Power BI placeholder until Azure/BI integration is finalized.
"""

import os
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium
import folium

def render(L):
    st.set_page_config(layout="wide", page_title="Redlining Visualizer", page_icon="📍")
    st.title(L.get("map_title", "📍 Redlining Map Viewer"))

    @st.cache_data
    def load_data():
        """Load redlining GeoJSON data from fallback paths."""
        paths_to_try = [
            os.path.join("data", "HOLC_Atlanta_GA.geojson"),
            os.path.join("data", "merged_housing_data.geojson")
        ]
        for path in paths_to_try:
            if os.path.exists(path):
                return gpd.read_file(path)
        st.error(L.get("map_error", "No redlining data found in expected paths."))
        st.stop()

    holc_gdf = load_data()

    # Sidebar Map Option
    map_type = st.sidebar.radio(
        L.get("map_provider", "Map Provider"),
        (L.get("powerbi_option", "Power BI (Coming Soon)"), L.get("folium_option", "Folium (Fallback)")),
        index=0
    )

    if map_type == L.get("powerbi_option", "Power BI (Coming Soon)"):
        st.info(L.get("powerbi_placeholder", "🚧 Power BI map will be embedded here once finalized by the data team."))
        st.image("https://via.placeholder.com/1000x600.png?text=Power+BI+Map+Coming+Soon", 
                caption=L.get("powerbi_caption", "Power BI Visualization Placeholder"))
    else:
        st_folium(create_folium_map(holc_gdf), width=1200, height=700)

    # Sidebar Stats
    st.sidebar.subheader(L.get("map_statistics", "Statistics"))
    if 'grade' in holc_gdf.columns:
        grade_counts = holc_gdf['grade'].value_counts()
        st.sidebar.metric(L.get("total_areas", "Total Areas"), len(holc_gdf))
        st.sidebar.metric(L.get("a_grade_areas", "A-Grade Areas"), grade_counts.get('A', 0))
        st.sidebar.metric(L.get("d_grade_areas", "D-Grade Areas"), grade_counts.get('D', 0))
    else:
        st.sidebar.warning(L.get("no_grade_column", "No 'grade' column found in data."))

def create_folium_map(gdf):
    """Create a Folium-based fallback map."""
    m = folium.Map(location=[33.749, -84.388], zoom_start=11)
    folium.GeoJson(
        gdf,
        style_function=lambda f: {
            'fillColor': {
                'A': '#00FF00', 'B': '#FFFF00',
                'C': '#FFA500', 'D': '#FF0000'
            }.get(f.get('properties', {}).get('grade', 'Unknown'), '#CCCCCC'),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        }
    ).add_to(m)
    return m
