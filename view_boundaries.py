import geopandas as gpd

# Load the shapefile
gdf = gpd.read_file('boundaries/recintos_municipales_inspire_peninbal_etrs89.shp')

# See all column names
print(gdf.columns)

# Look at the first few municipalities
print(gdf.head(10).to_string())

# Filter just Madrid region municipalities
madrid = gdf[gdf['CODNUT2'] == 'ES30']  # Madrid is ES30
print(madrid[['NAMEUNIT', 'NATCODE']].reset_index().to_string())
