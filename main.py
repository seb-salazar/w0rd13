import csv
import random

from getpass import getpass
from typing import List, Tuple


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


def select_random_word():
    global n_letters_allowed

    with open(f"./words/{n_letters_allowed}_letter_words.txt") as f:
        reader = csv.reader(f)
        words_list = list(reader)

    word = random.choice(words_list)[0]
    return word


def print_grid_and_words(area: int, unit: int, words_list: List[str]):
    """area (a): a x a grid. unit: the number of | of each box side"""
    global result_index_and_letters, day_word_list_with_indexes, day_word_list, user_word_list

    partial_matches  = set(day_word_list) & set(user_word_list)
    exact_matches: Tuple[int, str] = set(day_word_list_with_indexes) & set(result_index_and_letters)

    # Colour the letters
    word = list(words_list[-1])
    letters_ocurrences = {}
    letters_colouring_counter = {letter : 0 for letter in user_word_list}

    for index, found_letter in exact_matches:
        word[index] = bcolors.OKGREEN + found_letter + bcolors.ENDC
        letters_colouring_counter[found_letter] +=1

    for index, letter in enumerate(word):
        letters_ocurrences[letter] = day_word_list.count(letter)
        if letter in partial_matches and letters_colouring_counter[letter] < letters_ocurrences[letter]:
            user_word_list.count(letter)
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


def select_game_mode():
    global game_mode

    allowed_modes = (1, 2)
    try:
        print("--- Select your Game Mode ---\n")
        print("1 : SOLO mode (Guess the word from a random set of words)")
        print("2 : VERSUS mode (Your oponent has to guess your secret word)")
        print("\nSelect your game mode!")
        game_mode = int(input("Type 1 or 2 and press ENTER: "))
    except ValueError:
        print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: Please input a valid integer number")
        select_game_mode()

    if game_mode not in allowed_modes:
        print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: Please select a valide Game Mode")
        select_game_mode()


def play_again_query():
    response = str(input("Play again? [y/n]: "))
    print("")
    if response == "y":
        play_game()
    elif response == "n":
        exit()
    else:
        print(f"\n{bcolors.WARNING}Please input a valid response{bcolors.ENDC}")
        play_again_query()


def input_n_of_letters():
    global n_letters_allowed
    
    try:
        n_letters_allowed = int(input("\nNumber of letters allowed to play (5, 6, 7 or 8): "))
    except ValueError:
        print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: Please input a valid integer number")
        input_n_of_letters()

    if n_letters_allowed < 5:
        print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: The number of letters must be greater or equal than 5")
        input_n_of_letters()


def input_day_word():
    global game_mode, n_letters_allowed, day_word, day_word_list, day_word_list_with_indexes

    if game_mode == 1:
        day_word = select_random_word().upper()
        day_word_list = list(day_word)
    else:
        day_word = str(getpass("\nDay Word: " + "*" * n_letters_allowed)).upper()
        day_word_list = list(day_word)

    run_validations()
    day_word_list_with_indexes = [(index, letter) for index, letter in enumerate(day_word_list)]
    input_and_set()


def input_and_set():
    global counter, n_letters_allowed, user_word, user_word_list

    user_word = str(input(f"\nGuess the {n_letters_allowed} letter word (try {counter + 1}/5): ")).upper()
    user_word_list = list(user_word)
    run_validations()
    compare_and_yield_results()


def run_validations():
    global n_letters_allowed, day_word, day_word_list, user_word, user_word_list

    if day_word and not day_word.isalpha():
        print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: The word '{day_word}' is not valid word")
        input_day_word()

    if user_word and not user_word.isalpha():
        print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: The word '{user_word}' is not a valid word")
        input_and_set()

    if len(day_word_list) != n_letters_allowed:
        print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: The word '{day_word}' does not have the previously determined amount of letters ({n_letters_allowed})")
        input_day_word()

    if len(user_word_list) and len(user_word_list) != n_letters_allowed:
        print(f"\n{bcolors.FAIL}ERROR{bcolors.ENDC}: Word should be {n_letters_allowed} digits")
        input_and_set()


def compare_and_yield_results():
    global counter, n_letters_allowed, day_word, day_word_list, day_word_list_with_indexes, user_word_list, result_index_and_letters, words_try_list

    user_word = "".join(user_word_list)
    counter += 1

    words_try_list.append(user_word)

    result_index_and_letters = []
    for index, letter in enumerate(user_word_list):
        results = [
            (index, element)
            for _, element in day_word_list_with_indexes if element == letter
        ]
        result_index_and_letters += results

    result_index_and_letters = list(set(result_index_and_letters))
    partial_result_list = ["_ "]*n_letters_allowed
    for index, element in result_index_and_letters:
        partial_result_list[index] = element

    print_grid_and_words(n_letters_allowed, 1, words_try_list)

    if day_word == user_word:
        print(f"\nYou won! Congratulations! :D\n")
        play_again_query()

    if counter == 5:
        print(f"\nYou lost :(")
        print(f"The actual word was {bcolors.UNDERLINE + day_word + bcolors.ENDC}\n")
        play_again_query()

    input_and_set()


def play_game():
    global day_word, day_word_list, n_letters_allowed, result_index_and_letters, user_word, user_word_list, words_try_list, day_word_list_with_indexes, counter, game_mode

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

    print("\n\n\n**** WELCOME TO W0RD13 (EN Version)****\n\n\n")

    select_game_mode()
    input_n_of_letters()
    input_day_word()
    input_and_set()

if __name__ == "__main__":
    play_game()
