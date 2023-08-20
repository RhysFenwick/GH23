import pandas as pd
from normalisation import standardise

data = pd.read_csv("gumtree_counts.csv")
names = pd.read_csv("SA2_decoder.csv")

dictionary = names.set_index('Name').to_dict()['SA2']

new_names = []
counts = []
count = 0

for x in data["SA2_NAME21"]:
    if x in dictionary:
        new_names.append(dictionary[x])
        counts.append(data["Count"][count])
    count = count + 1

standardisecount = standardise(counts)

new_dataframe = pd.DataFrame({"SA2": new_names, "Gumtree": standardisecount})

new_dataframe.to_csv("normalised_gumtree_data.csv",index=False)

