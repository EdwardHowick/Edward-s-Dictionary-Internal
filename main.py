import os

WORD_BOOK_FILENAME = 'wordbook.txt'

try:
    open(WORD_BOOK_FILENAME)
except FileNotFoundError:
    print(f"Please ensure that {WORD_BOOK_FILENAME} exists in folder")
    print("Exiting...")
    os._exit(1)

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
        return endpoint.status_code == 200

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
            print("No antonyms found.")

class Favorites:
    def __init__(self, filename=WORD_BOOK_FILENAME):
        self.filename = filename
        try:
            with open(self.filename) as f:
                self.saved_words = f.read().splitlines()
        except FileNotFoundError:
            self.saved_words = []

    def upload_word(self, word_choice_save):
        with open(self.filename, "a") as f:
            f.write(word_choice_save + '\n')
            print("\nSuccessfully Saved!")

    def remove_word(self, word_to_remove):
        with open(WORD_BOOK_FILENAME) as f:
            savedwords_text = f.read()
        wordslist = savedwords_text.split()
        if word_to_remove in wordslist:
            wordslist.remove(word_to_remove)
            with open(self.filename, "w") as f:
                for word in wordslist:
                    f.write(word + "\n")
                print("Successfully Removed!")
        else:
            print("Word not found.")

    def view_favorites(self):
        with open(WORD_BOOK_FILENAME) as f:
            savedwords_text = f.read()
        word_list = savedwords_text.split()
        print("\n--Saved words--")
        for word in word_list:
            print(word)
        print()

def wordbook_remove_options():
    favorites_instance = Favorites()
    favorites_instance.view_favorites()
    while True:
        remove_choice = input("Enter 'm' for menu or 'x' to remove a word: ").lower()
        if remove_choice == "m":
            break
        elif remove_choice == "x":
            word_to_remove = input("Enter word to remove: ").capitalize()
            favorites_instance.remove_word(word_to_remove)
        else:
            print("\n--Invalid input--\n")

def menu():
    word_instance = Word()
    favorites_instance = Favorites()
    while True:
        print("\nWELCOME TO EDWARD'S ENGLISH DICTIONARY")
        print("Would you like to:")
        print("1. Search Word")
        print("2. Save Word")
        print("3. View Saved Words")
        print("4. Exit")
        choice = input("Enter Choice: ").lower()
        if choice == "1":
            word_choice = str(input("\nEnter Word:")).capitalize()
            if not word_instance.check_word_existence(word_choice):
                print(f"\nNo results for {word_choice}.")
            else:
                word_instance.get_definitions(word_choice)
                word_instance.get_synonyms(word_choice)
                word_instance.get_antonyms(word_choice)
        elif choice == "2":
            word_to_save = str(input("Enter word to save: ")).capitalize()
            if not word_instance.check_word_existence(word_to_save):
                print("\nWord not found.")
            else:
                favorites_instance.upload_word(word_to_save)
        elif choice == "3":
            with open(WORD_BOOK_FILENAME) as f:
                wordbook_text = f.read()
            wordbook_list = wordbook_text.split()
            if wordbook_list:
                wordbook_remove_options()
            else:
                print("\nNo words have been saved yet.")
        elif choice == "4":
            print("\nGoodbye...\n")
            os._exit(0)
        else:
            print("\nInvalid Choice.")

if __name__ == "__main__":
    menu()