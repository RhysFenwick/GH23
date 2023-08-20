import requests
import json


url = r"https://25uu0avefe.execute-api.ap-southeast-2.amazonaws.com/default"

payload = {
    "birth_weight": 1.5,
    "gum_weight": 0,
    "pop_weight": 1,
    "ses_weight": 2
}


try:
        # Make the POST request
        response = requests.post(url, params=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Request successful")
            print("Response content:")
            print(response.content.decode("utf-8"))  # Print response content as a string
        else:
            print(f"Request failed with status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")