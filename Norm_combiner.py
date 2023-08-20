import json
import io
from io import StringIO
import pandas as pd

file_loc = "C:\\Users\\Rhys\Downloads\\"

def s3_getter(filename):
    dataframe = pd.read_csv(file_loc+filename)
    print("Got "+filename)
    return(dataframe)



SES = s3_getter("normalised_SES_data.csv")
population = s3_getter("normalised_population_data.csv")
birth = s3_getter("normalised_birth_data.csv")
gum = s3_getter("normalised_gumtree_data.csv")
names = s3_getter("SA2_decoder.csv")
dictionary = names.set_index('SA2').to_dict()['Name']

new_birth = []
new_population = []
new_SES = []
new_locations = []
new_names = []
new_gums = []

for location in SES["SA2"]:
    if((location in birth["SA2"].to_list()) and (location in population["SA2"].to_list())):
        new_locations.append(location)
        new_birth.append(birth[birth["SA2"]==location]["Births"].to_list()[0])
        new_population.append(population[population["SA2"]==location]["Population"].to_list()[0])
        new_SES.append(SES[SES["SA2"]==location]["SES"].to_list()[0])
        new_names.append(names[names["SA2"]==location]["Name"].to_list()[0])
        try:
            new_gums.append(gum[gum["SA2"]==location]["Gumtree"].to_list()[0])
        except:
            new_gums.append("0")


new = pd.DataFrame({"Location": new_locations,"Births":new_birth,"Population":new_population,"SES":new_SES,"Name":new_names,"Gumtree":new_gums})
new.to_csv(file_loc+"norm_vals.csv")
overall_score = new["Births"] * new["Population"] * new["SES"]
# overall_score = new["Births"]**user_weights[0] * new["Population"]**user_weights[1] * new["SES"]**user_weights[2]
score_dataframe = pd.DataFrame({"Location": new_locations, "Score": overall_score})
# score_dataframe.to_csv("scores.csv",index=False)

sorted_scores = overall_score.to_list()
index = range(len(sorted_scores))
s = sorted(index, reverse=True, key=lambda i: sorted_scores[i])
best_values = (score_dataframe.loc[s[:5]]["Location"].to_list())
#print("The best places to set up are:")
loc_string = "The best places to set up are: "
for x in best_values:
    # print(dictionary[x])
    loc_string += dictionary[x]
    loc_string += ", "

loc_string = loc_string[0:-2]
print(loc_string)
        

