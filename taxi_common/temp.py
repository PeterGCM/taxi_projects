import geopandas as gpd

path = 'data/SG_maps/singapore_roads.geojson'

df = gpd.read_file(path)
print df.shape
df.plot()
