import requests
import json

url = "https://api.fda.gov/drug/label.json"
params = {
    "search": 'openfda.substance_name:"Enalapril"',
    "limit": 1
}

response = requests.get(url, params=params)
fda_data = response.json()

print(json.dumps(fda_data, indent=4))  # Daha okunabilir bir şekilde yazdır