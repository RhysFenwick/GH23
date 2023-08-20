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
START_X=-28
END_X=-37.5
START_Y=141
END_Y=154
X_ACC=1000
Y_ACC=1000
SERVICE_RANGE=.01
random.seed(random.randint(0,10000))
# Load the Australia shapefile
#australia_shapefile = gpd.read_file(r"/root/coding/govhack/data/AUS_2021_AUST_GDA2020.shp")
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
sa2_centroids=sa2_shapefile.representative_point()
#Outputs csv file containing points for each SA2 region.
print(sa2_centroids)
sa2_centroids.to_csv("points.csv")