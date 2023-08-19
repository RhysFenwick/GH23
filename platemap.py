import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Read the shapefile
gdf = gpd.read_file(r"C:\Users\61411\OneDrive\Desktop\Govhack\SA2_2021_AUST_GDA2020.shp")
gdf = gdf.set_index('SA2_CODE21')

SA_data = pd.read_csv("BirthsLevel2Cleaned.csv")

indexes = (SA_data["SA2_CODE21"])
new_indexes = []
for x in indexes:
    new_indexes.append(str(x))

SA_data["SA2_CODE21"] = new_indexes
SA_data = SA_data.set_index("SA2_CODE21")

merged = gdf.join(SA_data)

merged.plot(figsize=(5,5), column="Births - 2019")
plt.show()