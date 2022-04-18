from getpass import getpass
from typing import List, Tuple

from utils.string_utils import bcolors, select_random_word


class W0RD13:
    day_word = ""
    day_word_list = []
    n_letters_allowed = 0
    result_index_and_letters = []
    user_word = ""
    user_word_list = []
    words_try_list = []
    day_word_list_with_indexes = []
    counter = 0
    game_mode = 0

    def print_grid_and_words(cls, area: int, unit: int, words_list: List[str]):
        """area (a): a x a grid. unit: the number of | of each box side"""

        partial_matches  = set(cls.day_word_list) & set(cls.user_word_list)
        exact_matches: Tuple[int, str] = set(cls.day_word_list_with_indexes) & set(cls.result_index_and_letters)

        # Colour the letters
        word = list(words_list[-1])
        letters_ocurrences = {}
        letters_colouring_counter = {letter : 0 for letter in cls.user_word_list}

        for index, found_letter in exact_matches:
            word[index] = bcolors.OKGREEN + found_letter + bcolors.ENDC
            letters_colouring_counter[found_letter] +=1

        for index, letter in enumerate(word):
            letters_ocurrences[letter] = cls.day_word_list.count(letter)
            if letter in partial_matches and letters_colouring_counter[letter] < letters_ocurrences[letter]:
                cls.user_word_list.count(letter)
                word[index] = bcolors.WARNING + letter + bcolors.ENDC
                letters_colouring_counter[letter] +=1

        words_list[-1] = word
        rows_to_print = [("|   ") * unit * area] * area
        for index, word in enumerate(words_list):
            row_to_print = ""
            for letter in word:
                row_to_print += "|"*unit + f" {bcolors.BOLD + letter + bcolors.ENDC} "

            rows_to_print[index] = row_to_print

        print("")
        for index, _ in enumerate(range(5)):
            print(("+" + " - " * unit) * area + "+")
            print(rows_to_print[index] + "|")
        print(("+" + " - " * unit) * area + "+")


    def select_game_mode(cls):
        allowed_modes = (1, 2)
        try:
            print("--- Select your Game Mode ---\n")
            print("1 : SOLO mode (Guess the word from a random set of words)")
            print("2 : VERSUS mode (Your oponent has to guess your secret word)")
            print("\nSelect your game mode!")
            cls.game_mode = int(input("Type 1 or 2 and press ENTER: "))
        except ValueError:
            print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: Please input a valid integer number")
            cls.select_game_mode(cls)

        if cls.game_mode not in allowed_modes:
            print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: Please select a valide Game Mode")
            cls.select_game_mode(cls)


    def play_again_query(cls):
        response = str(input("Play again? [y/n]: "))
        print("")
        if response == "y":
            cls.play_game()
        elif response == "n":
            exit()
        else:
            print(f"\n{bcolors.WARNING}Please input a valid response{bcolors.ENDC}")
            cls.play_again_query(cls)


    def input_n_of_letters(cls):
        try:
            cls.n_letters_allowed = int(input("\nNumber of letters allowed to play (5, 6, 7 or 8): "))
        except ValueError:
            print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: Please input a valid integer number")
            cls.input_n_of_letters(cls)

        if cls.n_letters_allowed < 5:
            print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: The number of letters must be greater or equal than 5")
            cls.input_n_of_letters(cls)


    def input_day_word(cls):
        if cls.game_mode == 1:
            cls.day_word = select_random_word(word_length=cls.n_letters_allowed).upper()
            cls.day_word_list = list(cls.day_word)
        else:
            cls.day_word = str(getpass("\nDay Word: " + "*" * cls.n_letters_allowed)).upper()
            cls.day_word_list = list(cls.day_word)

        cls.run_validations(cls)
        cls.day_word_list_with_indexes = [(index, letter) for index, letter in enumerate(cls.day_word_list)]
        cls.input_and_set(cls)


    def input_and_set(cls):
        cls.user_word = str(input(f"\nGuess the {cls.n_letters_allowed} letter word (try {cls.counter + 1}/5): ")).upper()
        cls.user_word_list = list(cls.user_word)
        cls.run_validations(cls)
        cls.compare_and_yield_results(cls)


    def run_validations(cls):
        if cls.day_word and not cls.day_word.isalpha():
            print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: The word '{cls.day_word}' is not valid word")
            cls.input_day_word(cls)

        if cls.user_word and not cls.user_word.isalpha():
            print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: The word '{cls.user_word}' is not a valid word")
            cls.input_and_set(cls)

        if len(cls.day_word_list) != cls.n_letters_allowed:
            print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: The word '{cls.day_word}' does not have the previously determined amount of letters ({cls.n_letters_allowed})")
            cls.input_day_word(cls)

        if cls.user_word_list and len(cls.user_word_list) != cls.n_letters_allowed:
            print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: Word should be {cls.n_letters_allowed} digits")
            cls.input_and_set(cls)


    def compare_and_yield_results(cls):
        cls.counter += 1
        cls.words_try_list.append(cls.user_word)

        result_index_and_letters = []
        for index, letter in enumerate(cls.user_word_list):
            results = [
                (index, element)
                for _, element in cls.day_word_list_with_indexes if element == letter
            ]
            result_index_and_letters += results

        cls.result_index_and_letters = list(set(result_index_and_letters))
        partial_result_list = ["_ "] * cls.n_letters_allowed
        for index, element in cls.result_index_and_letters:
            partial_result_list[index] = element

        cls.print_grid_and_words(cls, cls.n_letters_allowed, 1, cls.words_try_list)

        if cls.day_word == cls.user_word:
            print(f"\nYou won! Congratulations! :D\n")
            cls.play_again_query(cls)

        if cls.counter == 5:
            print(f"\nYou lost :(")
            print(f"The actual word was {bcolors.UNDERLINE + cls.day_word + bcolors.ENDC}\n")
            cls.play_again_query(cls)

        cls.input_and_set(cls)

    def reset_variables(cls):
        cls.day_word = ""
        cls.day_word_list = []
        cls.n_letters_allowed = 0
        cls.result_index_and_letters = []
        cls.user_word = ""
        cls.user_word_list = []
        cls.words_try_list = []
        cls.day_word_list_with_indexes = []
        cls.counter = 0
        cls.game_mode = 0

    @classmethod
    def play_game(cls):
        cls.reset_variables(cls)

        print("\n\n\n**** WELCOME TO W0RD13 (EN Version)****\n\n\n")

        cls.select_game_mode(cls)
        cls.input_n_of_letters(cls)
        cls.input_day_word(cls)
        cls.input_and_set(cls)


if __name__ == "__main__":
    W0RD13.play_game()
