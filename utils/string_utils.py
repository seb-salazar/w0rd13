import csv
import random

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


def select_random_word(word_length: int):
    with open(f"./words/{word_length}_letter_words.txt") as f:
        reader = csv.reader(f)
        words_list = list(reader)

    word = random.choice(words_list)[0]
    return word
