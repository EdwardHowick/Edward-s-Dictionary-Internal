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
    """A class representing a word and it's properties."""

    def __init__(self):
        self.BASE_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

    def check_word_existence(self, word_choice):
        """This function is used to check whether a valid response is recieved from the requests to the api"""
        """By making a request to the api and returning a status code it can catch any errors with the request"""

        endpoint = self.make_request(word_choice)
        return endpoint.status_code == 200

    def make_request(self, word_choice):
        """This functions purpose is to make a request to the api and returns the data in the form of a endpoint variable"""
        endpoint_url = self.BASE_API_URL + word_choice
        try:
            endpoint = requests.get(endpoint_url) #sends request to api using url.
            return endpoint #retrieves data as endpoint variable.
        except:
            print("\nAPI call Failed. Please ensure that your internet is working and that you have disabled any active website blockers before running this program.\n")
            os._exit(1)

    def get_definitions(self, word_choice):
        """This function makes a request to the api for the users chosen word."""
        """Then retreives the data from the api in the form of the variable endpoint"""
        """Before changing the format of the data to be accessed in the form of lists"""
        """Lastly I just access the list of data and filter the definitions before displaying it to the user."""

        endpoint = self.make_request(word_choice) #makes request and retrives data.
        json_data = endpoint.json() #formats the data.
        print(f"\nDEFINITIONS of {word_choice}:")
        definitions = json_data[0]['meanings'][0]['definitions'] #filters the data.
        for definition in definitions[0:3]: #dislays data.
            print(f"-{definition['definition']}")

    def get_synonyms(self, word_choice):
        """The purpose of this function is to display the synonyms of a chosen word to the user"""
        
        endpoint = self.make_request(word_choice)
        """The purpose of this function is to make a request to the api for data on a word"""
        """This function first makes a request to the api for the users chosen word."""
        """Then retreives the data from the api in the form of the variable endpoint."""
        """Before using a function to change the format of the data to be accessed in the form of lists."""
        """Lastly I just access the list of data and filter the synonyms before displaying it to the user."""

        json_data = endpoint.json() #formats the data.
        synonyms = json_data[0]['meanings'][0]['synonyms'] #filters the data.
        print(f"\nSYNONYMS of {word_choice}:")
        if synonyms:#verifies synonyms found in dictionary.
            for synonym in synonyms: #displays data.
                print(f'-{synonym}')
        else:
            print("No synonyms found.")

    def get_antonyms(self, word_choice):
        """The purpose of this function is to display the antonyms of a chosen word to the user."""
        """Firstly this function retreives the data from the api in the form of the variable endpoint."""
        """Before using a function to change the format of the data to be accessed in the form of lists."""
        """Lastly it access the list of data and filters the synonyms before displaying it to the user."""

        endpoint = self.make_request(word_choice) #makes request and retrieves the data.
        json_data = endpoint.json() #formats the data
        antonyms = json_data[0]['meanings'][0]['antonyms'] #filters the data.
        print(f"\nANTONYMS of {word_choice}:")
        if antonyms: #verifies antonyms found in dictionary.
            for antonym in antonyms: #displays data.
                print(f'-{antonym}')
        else:
            print("No antonyms found.")


class WordBook:
    """A class representing a word book and its properties"""

    def __init__(self, filename=WORD_BOOK_FILENAME):
        """This function initializes the WorkBook class with a filename."""
        self.filename = filename
        with open(self.filename) as f:
            self.saved_words = f.read().splitlines()

    def view_favorites(self):
        """This function"""
        with open(WORD_BOOK_FILENAME) as f:
            savedwords_text = f.read()
        word_list = savedwords_text.split()
        print("\n--Saved words--")
        for word in word_list:
            print(word)
        print()

    def upload_word(self, word_choice_save):
        with open(self.filename, "a") as f:
            f.write(word_choice_save + '\n')
            print("\nSuccessfully Saved!")

    def remove_word(self, word_to_remove):
        with open(WORD_BOOK_FILENAME) as f:
            savedwords_text = f.read()
        wordbook_list = savedwords_text.split()
        if word_to_remove in wordbook_list:
            wordbook_list.remove(word_to_remove)
            with open(self.filename, "w") as f:
                for word in wordbook_list:
                    f.write(word + "\n")
                print("\nSuccessfully Removed!\n")
        else:
            print("\nWord not found.\n")


def wordbook_remove_options():
    wordbook_instance = WordBook()
    wordbook_instance.view_favorites()
    while True:
        remove_choice = input("Enter 'm' for menu or 'x' to remove a word: ").lower()

        if remove_choice == "m":
            break

        elif remove_choice == "x":
            word_to_remove = input("Enter word to remove: ").capitalize()
            wordbook_instance.remove_word(word_to_remove)
 
        else:
            print("\n--Invalid input--\n")

def menu():
    word_instance = Word()
    wordbook_instance = WordBook()
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
                wordbook_instance.upload_word(word_to_save)

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
            print("\n--Invalid Choice--")

if __name__ == "__main__":
    menu()