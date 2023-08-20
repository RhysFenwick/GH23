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

def numbers_with_commas_to_int(vector):
    new = []
    for x in vector:
        new.append(int("".join(x.split(","))))
    return(new)

def absolute_standardise(vector):
    count = 0
    indexes_of_bad_rows = []
    new = []
    for x in vector:
        if(x == "-"):
            indexes_of_bad_rows.append(count)
        else:
            new.append((4.5-np.abs(5.5-int(x)))/4.5)
        count = count + 1
    return(new, indexes_of_bad_rows)

def remove_bad_rows(vector, remove):
    new = []
    count = 0
    for x in vector:
        if(count not in remove):
            new.append(x)
        count = count + 1 
    return(new)


#Normalising birth data
birth_and_population_data = pd.read_csv("BirthsLevel2Cleaned.csv")
birth_data_2019 = birth_and_population_data["Births - 2019"]
birth_data_2019_standardised = standardise(birth_data_2019)
data_locations = birth_and_population_data["SA2_CODE21"]
new_birth_data = pd.DataFrame({"SA2":data_locations,"Births":birth_data_2019_standardised})
new_birth_data.to_csv("normalised_birth_data.csv", index=False)

#Normalising population data
population_data_2021 = birth_and_population_data["Total Resisdents - 2021"]
population_data_2021_int = numbers_with_commas_to_int(population_data_2021)
population_data_2021_standardised = standardise(population_data_2021_int)
new_population_data = pd.DataFrame({"SA2":data_locations,"Population":population_data_2021_standardised})
new_population_data.to_csv("normalised_population_data.csv", index=False)

#Normalising SES data
SES_data = pd.read_csv("SAL2SocioEconomicSummary2021.csv")
SES_data_unstandardised = SES_data["Decile of Index of Relative Socio-economic Disadvantage"]
SES_data_standardised, remove = absolute_standardise(SES_data_unstandardised)
SES_data_locations = remove_bad_rows(SES_data["2021 Statistical Area Level 2  (SA2) 9-Digit Code"], remove)
new_SES_data = pd.DataFrame({"SA2": SES_data_locations, "SES": SES_data_standardised})
new_SES_data.to_csv("normalised_SES_data.csv", index=False)