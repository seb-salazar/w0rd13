from getpass import getpass
from typing import List


def print_grid_and_words(area: int, unit: int, words_list: List[str]):
    """area (a): a x a grid. unit: the number of | of each box side"""

    rows_to_print = [("|   ") * unit * area] * area
    for index, word in enumerate(words_list):
        row_to_print = ""
        for letter in word:
            row_to_print += "|"*unit + f" {letter} "

        rows_to_print[index] = row_to_print

    for index, _ in enumerate(range(5)):
        print(("+" + " - " * unit) * area + "+")
        print(rows_to_print[index] + "|")
    print(("+" + " - " * unit) * area + "+")


def input_day_word():
    global day_word, day_word_list

    day_word = str(getpass("Day Word: ")).upper()
    day_word_list = list(day_word)
    run_validations()
    input_and_set()


def input_and_set():
    global n_letters_allowed, user_word_list

    user_word_list = list(str(input(f"Guess the {n_letters_allowed} letter word: ")).upper())
    run_validations()
    compare_and_yield_results()


def run_validations():
    global n_letters_allowed, day_word, day_word_list, user_word_list

    if len(day_word_list) != n_letters_allowed:
        print(f"ERROR: The word '{day_word}' does not have the previously determined amount of letters ({n_letters_allowed})")
        input_day_word()

    if len(user_word_list) and len(user_word_list) != n_letters_allowed:
        print(f"ERROR: Word should be {n_letters_allowed} digits")
        input_and_set()


def compare_and_yield_results():
    global counter, n_letters_allowed, day_word, day_word_list, user_word_list, result_index_and_letters, words_try_list

    user_word = "".join(user_word_list)
    counter += 1

    if day_word == user_word:
        print(f"You won! Congratulations!")
        exit()

    words_try_list.append(user_word)

    day_word_index_and_letters = list(enumerate(day_word_list))
    for letter in user_word_list:
        results = [
            (index, element)
            for index, element in day_word_index_and_letters if element == letter
        ]
        result_index_and_letters += results

    result_index_and_letters = list(set(result_index_and_letters))
    # print(result_index_and_letters)
    partial_result_list = ["_ "]*n_letters_allowed
    for index, element in result_index_and_letters:
        partial_result_list[index] = element

    partial_result_string = "".join(partial_result_list)
    
    # print(partial_result_string)

    print_grid_and_words(n_letters_allowed, 1, words_try_list)
    if counter == 5:
        print(f"You lost :(\nThe actual word was {day_word}")
        exit()

    input_and_set()


if __name__ == "__main__":
    day_word = ""
    day_word_list = []
    n_letters_allowed = int(input("Number of letters allowed: "))
    result_index_and_letters = []
    user_word_list = []
    words_try_list = []
    counter = 0

    input_day_word()
    input_and_set()
