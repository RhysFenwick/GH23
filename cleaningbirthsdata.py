import pandas as pd

data = pd.read_csv("BirthsLevel2Cleaned.csv")

count = 0

indexes = []

for SA2point in data["SA2"]:
    if(len(SA2point) == 9):
        indexes.append(count)
    count = count + 1

cleaned_data = data.loc[indexes]

cleaned_data.to_csv("BirthsLevel2Cleaned.csv")