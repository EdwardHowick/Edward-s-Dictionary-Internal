import os
import sys

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
        """Initializes the Word class with a URL"""
        self.BASE_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

    def check_word_existence(self, word_choice):
        """Checks whether a valid response is recieved from the requests.
        
        Parameters:
            word_choice (str): The word to check existence for.

        Returns:
            bool: True if the word exists, otherwise False.
        """

        endpoint = self.make_request(word_choice)
        return endpoint.status_code == 200 #returns true if word in dictionary, otherwise false

    def make_request(self, word_choice):
        """Makes a request to the api and returns the data in the form of a endpoint variable.
        
        Parameters:
            word_choice (str): The word to recieve data for.

        Returns:
            variable: The data for the word.
        """

        endpoint_url = self.BASE_API_URL + word_choice #creates the url to send to the api.
        try:
            endpoint = requests.get(endpoint_url) #sends request to api using url.
            return endpoint #retrieves data as endpoint variable.
        except:
            print("\nAPI call Failed. Please ensure that your internet is working and that you have disabled any active website blockers before running this program.\n")
            os._exit(1)

    def get_definitions(self, word_choice):
        """Displays the definitons of a chosen word to the user.
        
        Parameters:
            word_choice (str): The word to recieve data for.
        
        Returns:
            None
        """

        endpoint = self.make_request(word_choice) #makes request and retrives data.
        json_data = endpoint.json() #formats the data.
        print(f"\nDEFINITIONS of {word_choice}:")
        definitions = json_data[0]['meanings'][0]['definitions'] #filters the data.
        for definition in definitions[0:3]: #dislays data.
            print(f"-{definition['definition']}")

    def get_synonyms(self, word_choice):
        """Displays the synonyms of a chosen word to the user.

        Parameters:
            word_choice (str): The word to recieve data for.

        Returns:
            None
        """

        endpoint = self.make_request(word_choice) #makes request and retrieves the data.
        json_data = endpoint.json() #formats the data.
        synonyms = json_data[0]['meanings'][0]['synonyms'] #filters the data.
        print(f"\nSYNONYMS of {word_choice}:")
        if synonyms:#verifies synonyms are found in dictionary.
            for synonym in synonyms: #displays data.
                print(f'-{synonym}')
        else:
            print("No synonyms found.")

    def get_antonyms(self, word_choice):
        """Displays the antonyms of a chosen word to the user.
        
        Parameters:
            word_choice (str): The word to recieve data for.
        
        Returns:
            None
        """

        endpoint = self.make_request(word_choice) #makes request and retrieves the data.
        json_data = endpoint.json() #formats the data.
        antonyms = json_data[0]['meanings'][0]['antonyms'] #filters the data.
        print(f"\nANTONYMS of {word_choice}:")
        if antonyms: #verifies antonyms are found in dictionary.
            for antonym in antonyms: #displays data.
                print(f'-{antonym}')
        else:
            print("No antonyms found.")


class WordBook:
    """A class representing a word book and its properties."""

    def __init__(self, filename=WORD_BOOK_FILENAME):
        """Initializes the WordBook class with the WordBook filename and saved_words."""

        self.filename = filename
        with open(self.filename) as f:
            self.saved_words = f.read().splitlines()

    def view_wordbook(self):
        """Displays the wordbook to the user.
        
        Parameters:
            None
        
        Returns:
            None
        """

        print("\n--Saved words--")
        for word in self.saved_words: #displays wordbook.
            print(word)
        print()

    def upload_word(self, word_to_upload):
        """Uploads a word to the wordbook.txt file.
        
        Parameters:
            word_to_upload (str): The word to upload.
        
        Returns:
            None
        """

        with open(self.filename, "a") as f: #opens wordbook.txt text file and then appends the users word.
            f.write(word_to_upload + '\n')
            print("\nSuccessfully Saved!")

    def remove_word(self, word_to_remove):
        """Removes a word from the wordbook.txt file.
        
        Parameters:
            word_to_remove (str): The word to remove
        
        Returns:
            None
        """
        if word_to_remove in self.saved_words: #makes sure the word to remove is in the wordbook list.
            self.saved_words.remove(word_to_remove) #removes the word from the wordbook list.
            with open(self.filename, "w") as f: #opens the wordbook text file in the write format.
                for word in self.saved_words: #overrides the old wordbook.txt text file with the new wordbook list.
                    f.write(word + "\n")
                print("\nSuccessfully Removed!\n")
        else:
            print("\nWord not found.\n")


def wordbook_remove_options():
    """Sub-menu for the user to remove a word."""

    wordbook_instance = WordBook()
    wordbook_instance.view_wordbook()
    while True: #remove options loop
        remove_choice = input("Enter 'm' for menu or 'x' to remove a word: ").lower()

        if remove_choice == "m": #returns the user to menu.
            break

        elif remove_choice == "x": #allows user to remove a word.
            word_to_remove = input("Enter word to remove: ").capitalize()
            wordbook_instance.remove_word(word_to_remove) #removes word.
 
        else:
            print("\n--Invalid input--\n")

def menu():
    """Main menu for english dictionary."""

    word_instance = Word()
    wordbook_instance = WordBook()
    while True:
        print("\nWELCOME TO EDWARD'S ENGLISH DICTIONARY")
        print("Would you like to:")
        print("1. Search Word")
        print("2. Save Word")
        print("3. View WordBook")
        print("4. Exit")
        choice = input("Enter Choice: ").lower() #input for branch choice.

        if choice == "1": #search word branch
            word_choice = str(input("\nEnter Word:")).capitalize()
            if not word_instance.check_word_existence(word_choice):
                print(f"\nNo results for {word_choice}.")
            else:
                word_instance.get_definitions(word_choice)
                word_instance.get_synonyms(word_choice)
                word_instance.get_antonyms(word_choice)

        elif choice == "2": #save word branch
            word_to_upload = str(input("Enter word to save: ")).capitalize()
            if not word_instance.check_word_existence(word_to_upload):
                print("\nWord not found.")
            else:
                wordbook_instance.upload_word(word_to_upload)

        elif choice == "3": #view wordbook branch
            with open(WORD_BOOK_FILENAME) as f:
                wordbook_text = f.read()
            wordbook_list = wordbook_text.split()
            if wordbook_list:
                wordbook_remove_options()
            else:
                print("\nNo words have been saved yet.")

        elif choice == "4": #exit branch
            print("\nGoodbye...\n")
            os._exit(0)

        else:
            print("\n--Invalid Choice--")

if __name__ == "__main__":
    menu()