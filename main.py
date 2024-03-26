import os

try:
    import requests
except ImportError:
    print("Please install the requests package by running:")
    print("pip install requests")
    print("This program cannot run without the requests package.")
    print("Exiting...")
    os._exit(1)



BASE_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
WORD = f"meow"


response = requests.get(BASE_API_URL + WORD)
 

if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print("API call failed.")