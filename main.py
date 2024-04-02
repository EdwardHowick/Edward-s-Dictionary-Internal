import os
import requests
saved_words_filename = 'savedwords.txt'

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
    

    def check_word_existence(self, word_choice):
        endpoint = self.make_request(word_choice)
        if endpoint.status_code == 200:
            return True
        else:
            return False

    def make_request(self, word_choice):
        endpoint_url = self.BASE_API_URL + word_choice
        endpoint = requests.get(endpoint_url)
        return endpoint

    def get_definitions(self, word_choice):
        endpoint = self.make_request(word_choice)
        json_data = endpoint.json()
        print(f"\nDEFINITIONS of {word_choice}:")
        definitions = json_data[0]['meanings'][0]['definitions']
        for definition in definitions[0:3]:
            print(f"-{definition['definition']}")

    def get_synonyms(self, word_choice):
        endpoint = self.make_request(word_choice)
        json_data = endpoint.json()
        synonyms = json_data[0]['meanings'][0]['synonyms']
        print(f"\nSYNONYMS of {word_choice}:")
        if synonyms:
            for synonym in synonyms:
                print(f'-{synonym}')
        else:
            print("No synonyms found.")

    def get_antonyms(self, word_choice):
        endpoint = self.make_request(word_choice)
        json_data = endpoint.json()
        antonyms = json_data[0]['meanings'][0]['antonyms']
        print(f"\nANTONYMS of {word_choice}:")
        if antonyms:
            for antonym in antonyms:
                print(f'-{antonym}')
        else:
            print("No antonyms")

class Favorites:
    def __init__(self, filename='savedwords.txt'):
        self.filename = filename
        try:
            with open(self.filename) as f:
                self.saved_words = f.read().splitlines()
        except FileNotFoundError:
            self.saved_words = []
    
    def upload_word(self, word_choice_save):
        with open(self.filename, "a") as f:
            f.write(word_choice_save + '\n')
            print("\nSuccessfully Added.")

    def remove_word():
        pass
    def view_favorites(self):
        try:
            with open(saved_words_filename) as f:
                savedwords_text = f.read()
        except:
            savedwords_text = ''
        word_list = savedwords_text.split()
        print("Saved words:")
        for word in word_list:
            print(word)


def menu():
    wordapi = Word()
    favoritesapi = Favorites()
    while True:
        print("\nWELCOME TO EDWARD'S ENGLISH DICTIONARY")
        print("Would you like to:")
        print("1. Search Word")
        print("2. Save Word")
        print("3. View Saved Words")
        print("4. Exit")
        choice = input("Enter Choice: ").lower()
        if choice == "1":
            word_choice = str(input("\nEnter Word:"))
            if not wordapi.check_word_existence(word_choice):
                print(f"\nNo results for {word_choice}.")
            else:
                wordapi.get_definitions(word_choice)
                wordapi.get_synonyms(word_choice)
                wordapi.get_antonyms(word_choice)
        elif choice == "2":
            word_choice_save = str(input("Enter word to save: "))
            favoritesapi.upload_word(word_choice_save)
        elif choice == "3":
            favoritesapi.view_favorites()
        elif choice == "4":
            print("\nGoodbye...\n")
            os._exit(0)
        else:
            print("\nInvalid Choice.")
if __name__ == "__main__":
    menu()