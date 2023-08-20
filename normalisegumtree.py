import pandas as pd

data = pd.read_csv("gumtree_counts.csv")
names = pd.read_csv("SA2_decoder.csv")

dictionary = names.set_index('Name').to_dict()['SA2']

print(data)