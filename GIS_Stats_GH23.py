import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


list_of_normalised_data = []

# Takes location of stats csv and column heading of the thing you care about, returns normalised list of thing you care about
def csv_data_extractor(csv_loc,stat):
    csv = pd.read_csv(csv_loc)
    dat = csv[stat].tolist()
    m_dat = max(dat)
    for i in dat:
        i = i/m_dat
    list_of_normalised_data.append(dat)


# takes list of lists of factors to weight (each sub-list is the weightings for each SA2 area) and returns overall weights
def factor_weighter(weights_l_of_l):
    weightslist = []
    for i in range(len(weights_l_of_l[0])):
        init = 1
        for j in weights_l_of_l:
            init *= j[i]
        weightslist.append(init)
    gdf["Weights"]=weightslist
        


# Read the shapefile
gdf = gpd.read_file(r"C:\Users\Rhys\Downloads\SA2_2021_AUST_SHP_GDA2020\SA2_2021_AUST_GDA2020.shp")
SA_data_loc = r"C:\Users\Rhys\Downloads\21_Fert_Data.csv"

csv_data_extractor(SA_data_loc, "Birthrate")
factor_weighter(list_of_normalised_data)

print(gdf)

gdf.plot(figsize=(5,5), column="Weights")
plt.show()