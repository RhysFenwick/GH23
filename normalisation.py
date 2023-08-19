import pandas as pd
import numpy as np

def standardise(vector):
    min = np.min(vector)
    max = np.max(vector)
    difference = max-min
    new_vector = []
    for x in vector:
        new_vector.append((x-min)/difference)
    return(new_vector)

#Normalising birth data
birth_data = pd.read_csv("BirthsLevel2Cleaned.csv")
birth_data_2019 = birth_data["Births - 2019"]
birth_data_2019_standardised = standardise(birth_data_2019)
birth_data_locations = birth_data["SA2_CODE21"]
normalised_birth_data = pd.DataFrame({"SA2":birth_data_locations,"Births":birth_data_2019_standardised})
normalised_birth_data.to_csv("normalised_birth_data.csv", index=False)

