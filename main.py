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


def replace_str_at_position(string: str, new_character: str, position: int):
    string = string[:position] + new_character + string[position+1:]
    return string


def print_grid_and_words(area: int, unit: int, words_list: List[str]):
    """area (a): a x a grid. unit: the number of | of each box side"""
    global result_index_and_letters, day_word_list_with_indexes, day_word_list, user_word_list

    partial_matches  = set(day_word_list) & set(user_word_list)
    exact_matches: Tuple[int, str] = set(day_word_list_with_indexes) & set(result_index_and_letters)

    # Colour the letters
    word = list(words_list[-1])
    for index, letter in enumerate(word):
        if letter in partial_matches and letter not in list(sum(exact_matches, ())):
            word[index] = bcolors.WARNING + letter + bcolors.ENDC

    for index, found_letter in exact_matches:
        word[index] = bcolors.OKGREEN + found_letter + bcolors.ENDC

    words_list[-1] = word
    rows_to_print = [("|   ") * unit * area] * area
    for index, word in enumerate(words_list):
        row_to_print = ""
        for letter in word:
            row_to_print += "|"*unit + f" {bcolors.BOLD + letter + bcolors.ENDC} "

        rows_to_print[index] = row_to_print

    for index, _ in enumerate(range(5)):
        print(("+" + " - " * unit) * area + "+")
        print(rows_to_print[index] + "|")
    print(("+" + " - " * unit) * area + "+")


def input_n_of_letters():
    global n_letters_allowed
    
    try:
        n_letters_allowed = int(input("Number of letters allowed: "))
    except ValueError:
        print(f"ERROR: Please input a valid integer number")
        input_n_of_letters()

    if n_letters_allowed < 5:
        print(f"ERROR: The number of letters must be greater or equal than 5")
        input_n_of_letters()


def input_day_word():
    global n_letters_allowed, day_word, day_word_list, day_word_list_with_indexes

    day_word = str(getpass("Day Word: " + "*" * n_letters_allowed)).upper()
    day_word_list = list(day_word)
    run_validations()
    day_word_list_with_indexes = [(index, letter) for index, letter in enumerate(day_word_list)]
    input_and_set()


def input_and_set():
    global n_letters_allowed, user_word, user_word_list

    user_word = str(input(f"Guess the {n_letters_allowed} letter word: ")).upper()
    user_word_list = list(user_word)
    run_validations()
    compare_and_yield_results()


def run_validations():
    global n_letters_allowed, day_word, day_word_list, user_word, user_word_list

    if day_word and not day_word.isalpha():
        print(f"ERROR: The word '{day_word}' is not valid word")
        input_day_word()

    if user_word and not user_word.isalpha():
        print(f"ERROR: The word '{user_word}' is not a valid word")
        input_and_set()

    if len(day_word_list) != n_letters_allowed:
        print(f"ERROR: The word '{day_word}' does not have the previously determined amount of letters ({n_letters_allowed})")
        input_day_word()

    if len(user_word_list) and len(user_word_list) != n_letters_allowed:
        print(f"ERROR: Word should be {n_letters_allowed} digits")
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
        print(f"You won! Congratulations! :D")
        exit()

    if counter == 5:
        print(f"You lost :(\nThe actual word was {day_word}")
        exit()

    input_and_set()


if __name__ == "__main__":
    day_word = ""
    day_word_list = []
    n_letters_allowed = 0
    result_index_and_letters = []
    user_word = ""
    user_word_list = []
    words_try_list = []
    day_word_list_with_indexes = []
    counter = 0

    input_n_of_letters()
    input_day_word()
    input_and_set()
