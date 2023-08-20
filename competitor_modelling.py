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
fig, axs = plt.subplots()
plt.tight_layout()
sa2_shapefile.plot(figsize=(10,10))
ax = plt.gca()
colors=[100,150,60,0]
sa2_centroids.plot(figsize=(10,10),ax=ax,alpha=0.1,c='red')
nx,ny=(X_ACC,Y_ACC)
x=np.linspace(START_X,END_X,nx)
y=np.linspace(START_Y,END_Y,ny)
positions=np.array(np.meshgrid(x,y)).T.reshape(-1,2)
print("positions: "+str(positions))
x_new=[]
y_new=[]
for pos in positions:
    x_new.append(pos[0])
    y_new.append(pos[1])
df = pd.DataFrame(
    {'Latitude': x_new,
     'Longitude': y_new})
print(df)
df['Coordinates'] = list(zip(df.Longitude, df.Latitude))
df['Coordinates'] = df['Coordinates'].apply(Point)
gdf = gpd.GeoDataFrame(df, geometry='Coordinates')
gdf.plot(ax=ax, color='yellow',alpha=0.01)
print("YES!!!!!!!")
plt.show()
plt.savefig("map.png")
# Set limits and number of points in grid
SERVICE_RANGE=1

def getDistanceBetween(points, point):
    if (point is not None):
        return point.distance(points)
    else:
        return 0
print(list(sa2_centroids))
for point in list(sa2_centroids):
    #print(point)
        print(getDistanceBetween(sa2_centroids,point))
#Make random list of coordinates, within Australia check if it's in shape, remove if it is, else keep.
sources=[]

for i,centroid in enumerate(list(sa2_centroids)):
    if (centroid is not None):
        sources.append([sa2_shapefile['Score'][i],(centroid.x, centroid.y)[0],(centroid.x, centroid.y)[1]])
print(sources)

def gauss2d(x, y, mx=0, my=0, sx=1, sy=1):
    return 1. / (2. * np.pi * sx * sy) * np.exp(-((x - mx)**2. / (2. * sx**2.) + (y - my)**2. / (2. * sy**2.)))
best_points=[]
p=np.zeros(shape=(X_ACC,Y_ACC), dtype=float)
max_source=0
randomint=random.randint(0,998)
sourceval=np.zeros(len(sources))
for i,sourcei in enumerate(sources):
    for j,sourcej in enumerate(sources):
        if j!=i:
            sourceval[i]+=sourcej[0]*gauss2d(sourcei[1],sourcei[2],sourcej[1],sourcej[2],SERVICE_RANGE,SERVICE_RANGE)
        else:
            sourceval[i]+=sourcei[0]
#Now, get differences and merge
sourceval/=max(sourceval)
print("source values: "+str(sourceval))
N_STORES=len(sources)
DAMPING_FACTOR=0.5
#Now, print out best and subtract once store is open there
best_SA2_regions=[]
print(np.arange(0,N_STORES,1))
for n in np.arange(0,N_STORES,1):
    print(n)
    maxarg=sourceval.argmax()
    best_SA2_regions.append(maxarg)
    for i,sourcei in enumerate(sourceval):
        if (i==maxarg):
            sourceval[i]-=DAMPING_FACTOR
        else:
            #print(gauss2d(sources[i][1],sources[i][2],sources[maxarg][1],sources[maxarg][2],SERVICE_RANGE,SERVICE_RANGE))
            sourceval[i]-=DAMPING_FACTOR*gauss2d(sources[i][1],sources[i][2],sources[maxarg][1],sources[maxarg][2],SERVICE_RANGE,SERVICE_RANGE)
    sourceval=(sourceval-min(sourceval))/(max(sourceval)-min(sourceval))
    print("source val:"+str(sourceval))
print(best_SA2_regions)
colsource=[]
for i in np.arange(len(best_SA2_regions)):
    colsource[i]=np.exp(-1/np.where(best_SA2_regions == i))
axes = plt.gca()
plt.tight_layout()
scatter(sources.T[1],sources.T[2],sources.T[0],c=colsource,alpha=1)
plt.savefig("test.png")