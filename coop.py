import streamlit as st
import pandas as pd
import folium
from folium.plugins import Search
from geojson import Point, Feature, FeatureCollection, dump
from streamlit_folium import folium_static

# Title
st.title("US Co-ops Map")

# Read the CSV file from the raw GitHub URL
df = pd.read_csv("https://raw.githubusercontent.com/rmkenv/Coops_streamlit/main/coops.csv")

# Filter out invalid values
df = df.dropna(subset=['Latitude', 'Longitude'])
df['Latitude'].fillna(0, inplace=True)
df['Longitude'].fillna(0, inplace=True)

# Convert DataFrame rows into GeoJSON features
features = []
for _, row in df.iterrows():
    point = Point((row["Longitude"], row["Latitude"]))
    properties = {
        "name": row["name_clean"],
        "phone": row["phone"],
        "email": row["email"]
    }
    features.append(Feature(geometry=point, properties=properties))

# Create a FeatureCollection from the list of features
feature_collection = FeatureCollection(features)

# Initialize a base map
m = folium.Map(location=[0, 0], zoom_start=2)

# Add the GeoJSON data directly to the map
geojson_layer = folium.GeoJson(feature_collection, name="geojson").add_to(m)

# Iterate over features to add markers with popups
for feature in feature_collection['features']:
    lon, lat = feature['geometry']['coordinates']
    name = feature['properties']['name']
    phone = feature['properties']['phone']
    email = feature['properties']['email']
    popup_content = f"Name: {name}<br>Phone: {phone}<br>Email: {email}"
    folium.Marker([lat, lon], popup=popup_content).add_to(m)

# Add the search tool
search = Search(
    layer=geojson_layer,
    geom_type='Point',
    placeholder="Search for a location",
    collapsed=False,
    search_label='name',
    search_zoom=8
).add_to(m)

# Display the map in Streamlit
folium_static(m)
