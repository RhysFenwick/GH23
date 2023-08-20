import json
import boto3
import io
from io import StringIO
import pandas as pd
import numpy

s3_client = boto3.client('s3')
bucket = "roundabout-bucket"

def s3_getter(filename):
    object = s3_client.get_object(Bucket=bucket, Key=filename)
    body = object['Body']
    csv_string = body.read().decode('utf-8')
    dataframe = pd.read_csv(StringIO(csv_string))
    print("Got "+filename)
    return(dataframe)


def lambda_handler(event, context):
    
    vals = s3_getter("norm_vals.csv")
    
    weights = event["rawQueryString"].split("&")
    birth_weight = float(weights[0].split("=")[1])
    gum_weight = float(weights[1].split("=")[1])
    pop_weight = float(weights[2].split("=")[1])
    ses_weight = float(weights[3].split("=")[1])
    
    vals["B_Ex"] = numpy.float_power(vals["Births"],birth_weight)
    vals["G_Ex"] = numpy.float_power(vals["Gumtree"],gum_weight)
    vals["P_Ex"] = numpy.float_power(vals["Population"],pop_weight)
    vals["S_Ex"] = numpy.float_power(vals["SES"],ses_weight)


    overall_score = round((vals["B_Ex"]+0.1) * (vals["G_Ex"]+0.1) * (vals["P_Ex"]+0.1) * (vals["S_Ex"]+0.1) * 100)
    score_dataframe = pd.DataFrame({"Name": vals["Name"], "Location":vals["Location"], "Score": overall_score})
    
    """sorted_scores = overall_score.to_list()
    index = range(len(sorted_scores))
    s = sorted(index, reverse=True, key=lambda i: sorted_scores[i])
    best_values = (score_dataframe.loc[s[:5]]["Name"].to_list())
    loc_string = "The best places to set up are: "
    for x in best_values:
        loc_string += x
        loc_string += "; "
    
    loc_string = loc_string[0:-2]
    print(loc_string)
    """
    wstring = ""
    
    for ind in score_dataframe.index:
        print(score_dataframe["Score"][ind])
        for i in range(score_dataframe["Score"][ind].astype(numpy.int64)):
            wstring += score_dataframe["Location"][ind].astype("str") + ","

    return {
        'statusCode': 200,
        'body': wstring
    }