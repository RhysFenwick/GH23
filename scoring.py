import pandas as pd

birth = pd.read_csv("normalised_birth_data.csv")
population = pd.read_csv("normalised_population_data.csv")
SES = pd.read_csv("normalised_SES_data.csv")

new_birth = []
new_population = []
new_SES = []
new_locations = []

for location in SES["SA2"]:
    if((location in birth["SA2"].to_list()) and (location in population["SA2"].to_list())):
        new_locations.append(location)
        new_birth.append(birth[birth["SA2"]==location]["Births"].to_list()[0])
        new_population.append(population[population["SA2"]==location]["Population"].to_list()[0])
        new_SES.append(SES[SES["SA2"]==location]["SES"].to_list()[0])

new = pd.DataFrame({"Location": new_locations,"Births":new_birth,"Population":new_population,"SES":new_SES})
overall_score = new["Births"] * new["Population"] * new["SES"]
score_dataframe = pd.DataFrame({"Location": new_locations, "Score": overall_score})
score_dataframe.to_csv("scores.csv",index=False)