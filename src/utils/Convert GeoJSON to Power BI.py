import geopandas as gpd
df = gpd.read_file("merged_housing_data.geojson")
df['longitude'] = df.geometry.centroid.x
df['latitude'] = df.geometry.centroid.y
df.drop(columns='geometry').to_csv("redlining_data_for_powerbi.csv", index=False)