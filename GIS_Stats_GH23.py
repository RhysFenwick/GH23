import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Read the shapefile
gdf = gpd.read_file(r"C:\Users\Rhys\Downloads\SA2_2021_AUST_SHP_GDA2020\SA2_2021_AUST_GDA2020.shp")
SA_data = pd.read_csv(r"C:\Users\Rhys\Downloads\BirthsLevel2Cleaned.csv")
merged = gdf.set_index('SA2_CODE21').join(SA_data.set_index('SA2'))
# print(merged)


merged.plot(figsize=(5,5), column="Births - 2019")
plt.show()