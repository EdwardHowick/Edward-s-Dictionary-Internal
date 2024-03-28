import os
import requests

try:
    import requests
except ImportError:
    print("Please install the requests package by running:")
    print("pip install requests")
    print("This program cannot run without the requests package.")
    print("Exiting...")
    os._exit(1)

class Word:
    def __init__(self):
        self.BASE_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    
    def make_request(self, word_choice):
        endpoint_url = self.BASE_API_URL + word_choice
        endpoint = requests.get(endpoint_url)
        return endpoint

    def get_definitions(self, word_choice):
        endpoint = self.make_request(word_choice)
        if endpoint.status_code == 200:
            json_data = endpoint.json()
            print(f"\nDEFINITIONS of {word_choice}:")
            definitions = json_data[0]['meanings'][0]['definitions']
            for definition in definitions[0:3]:
                print(f"-{definition['definition']}")
        else:
            print("API call failed.")

    def get_synonyms(self, word_choice):
        endpoint = self.make_request(word_choice)
        if endpoint.status_code == 200:
            json_data = endpoint.json()
            synonyms = json_data[0]['meanings'][0]['synonyms']
            print(f"\nSYNONYMS of {word_choice}:")
            if synonyms:
                for synonym in synonyms:
                    print(f'-{synonym}')
            else:
                print("-Null")
        else:
            print("API call failed.")

    def get_antonyms(self, word_choice):
        endpoint = self.make_request(word_choice)
        if endpoint.status_code == 200:
            json_data = endpoint.json()
            antonyms = json_data[0]['meanings'][0]['antonyms']
            print(f"\nANTONYMS of {word_choice}:")
            if antonyms:
                for antonym in antonyms:
                    print(f'-{antonym}')
            else:
                print("-Null")
        else:
            print("API call failed.")

class Wordsave:
    pass

def menu():
    api = Word()
    while True:
        print("\nWELCOME TO EDWARD'S ENGLISH DICTIONARY")
        print("Would you like to:")
        print("1. Search Word")
        print("2. Save Word")
        print("3. View Saved Words")
        print("4. Exit")
        choice = input("Enter Choice: ").lower()
        if choice == "1":
            word_choice = input("\nEnter Word:")
            api.get_definitions(word_choice)
            api.get_synonyms(word_choice)
            api.get_antonyms(word_choice)
        elif choice == "2":
            pass
        elif choice == "3":
            print("\nGoodbye...\n")
            os._exit(0)
        else:
            print("\nInvalid Choice\n")
if __name__ == "__main__":
    menu()