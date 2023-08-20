import requests
import csv
import json


# All states besides NSW/ACT have Aus-wide bounding box because we don't care about them at the moment
state_coords = {
     "QLD":"-55,72|-9,168",
     "NSW":"-37,140|-28,154",
     "ACT":"-36,148|-35,150",
     "SA":"-55,72|-9,168",
     "NT":"-55,72|-9,168",
     "TAS":"-55,72|-9,168",
     "VIC":"-55,72|-9,168",
     "WA":"-55,72|-9,168",
}

url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

# Key is a secret in the GitHub repo
def gMapper(original_suburb, original_state):

    payload = {
        "key": "FAKE_KEY",
        "input": original_suburb,
        "fields": "geometry",
        "inputtype": "textquery",
        "locationbias":f"rectangle:{state_coords[original_state]}"
    }

    try:
            # Make the POST request
            response = requests.post(url, params=payload)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                try:
                    # geom = json.loads(response.content.decode("utf-8"))["candidates"][0]["geometry"]["location"]
                    geom = json.loads(response.content.decode("utf-8"))["candidates"][0]["geometry"]["location"]
                    print(geom)
                    return(geom)
                except:
                    print(response.content.decode("utf-8"))
                    return({"lat":0,"lng":0})
            else:
                print(f"Request failed with status code: {response.status_code}")
                return({"lat":0,"lng":0})
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")




input_filename = r"C:\Users\Rhys\Downloads\output.csv"
output_filename = r"C:\Users\Rhys\Downloads\corrected_locations.csv"

try:
    with open(input_filename, "r", newline="") as input_file:
        reader = csv.DictReader(input_file)
        headers = reader.fieldnames
        rows = list(reader)

    for row in rows:
        original_suburb = row["Suburb"]
        original_state = row["State"]


        transformed_value = gMapper(original_suburb, original_state)
        row["Lat"] = transformed_value["lat"]
        row["Long"] = transformed_value["lng"]
        # row["Location"] = transformed_value

        with open(output_filename, "a", newline="") as output_file:
            writer = csv.writer(output_file, delimiter=' ')
            writer.writerow([transformed_value["lat"], transformed_value["lng"]])

    print("CSV transformation completed. Output written to", output_filename)

except FileNotFoundError:
    print(f"File '{input_filename}' not found.")

