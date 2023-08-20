import numpy as np
import matplotlib.pyplot as plt
import random
import scipy as sp
import sys
from scipy.ndimage.filters import gaussian_filter
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.geometry as sg
import shapely.ops as so
from geopandas import GeoSeries
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopandas.tools import sjoin
from matplotlib.pyplot import scatter
from shapely.geometry import shape, Point

#Load gumtree location data with lat and long
gumtree_data=pd.read_csv("/root/coding/govhack/data/corrected_locations.csv")

#Load NSW SA2 shapefile
sa2_shapefile = gpd.read_file(r"/root/coding/govhack/data/SA2_2021_AUST_GDA2020.shp")
#australia_shapefile = australia_shapefile.to_crs(epsg=4326)
sa2_shapefile = sa2_shapefile.to_crs(epsg=4326)
print(sa2_shapefile)
sa2_shapefile = sa2_shapefile.set_index('SA2_CODE21')
SA_data =pd.read_csv("/root/coding/govhack/data/scores.csv")
indexes = (SA_data["SA2_CODE21"])
new_indexes = []
for x in indexes:
    new_indexes.append(str(x))
SA_data["SA2_CODE21"] = new_indexes
SA_data = SA_data.set_index("SA2_CODE21")
print(sa2_shapefile)
sa2_shapefile = (sa2_shapefile.join(SA_data))
sa2_shapefile.dropna(inplace=True)
print(sa2_shapefile)
print(type(sa2_shapefile))

#Check which shape the gumtree data is in
def check(lon, lat, shape):
    # build a shapely point from your geopoint
    point = Point(lon, lat)
    # the contains function does exactly what you want
    return shape.contains(point)

# get the shapes
longs=list(gumtree_data['Longitude'])
lats=list(gumtree_data['Latitude'])
# build a shapely polygon from your shape
counts={}
print(sa2_shapefile)
for i,shape in enumerate(sa2_shapefile['geometry']):
    for j,long in enumerate(longs):
        if (check(longs[j],lats[j],shape)):
            if sa2_shapefile["SA2_NAME21"][i] in counts.keys():
                counts[sa2_shapefile["SA2_NAME21"][i]]=counts[sa2_shapefile["SA2_NAME21"][i]]+1
            else:
                counts[sa2_shapefile["SA2_NAME21"][i]]=1
pd.DataFrame(counts.items()).to_csv("gumtree_counts.csv")