import re
import argparse
import getpass
import string

from data_loaders import load_list_from_file, try_get_list_from_file


def parse_args():
    parser = argparse.ArgumentParser(
        description='This script calc the strength of your password.')
    parser.add_argument(
        '-bl',
        '--blacklist_path',
        help='Txt file with passwords blacklist, separated by new line'
    )
    parser.add_argument(
        '-fl',
        '--forbiddenlist_path',
        help='Txt file with abbreviations, birthdays and so on, '
             'separated by new line'
    )

    return parser.parse_args()


def is_special(char):
    all_normal_chars = string.ascii_letters + string.digits
    return char not in all_normal_chars


def compose_regex_list():
    upper_and_lower_chars = r'(?=[A-Z]*[a-z])(?=[a-z]*[A-Z])[a-zA-Z]'
    more_than_eight_word_length = r'\S{8,}'
    numbers_chars = r'\d'
    regex_list = [
        upper_and_lower_chars,
        more_than_eight_word_length,
        numbers_chars
    ]
    return regex_list


def calc_password_strength(password, blacklist, forbidden_list):
    password_strength_min = 0
    password_strength_max = 10

    if password in blacklist:
        return password_strength_min

    password_strength = password_strength_max

    for regex in compose_regex_list():
        if not re.search(regex, password):
            password_strength -= 2
    for word in forbidden_list:
        if re.search(word, password):
            password_strength -= 1

    spec_chars = [char for char in password if is_special(char)]
    if not spec_chars:
        password_strength -= 2

    return max(password_strength_min, password_strength)


if __name__ == '__main__':
    args = parse_args()
    blacklist_filepath = args.blacklist_path
    forbidden_list_filepath = args.forbiddenlist_path
    username = input('Type your username: ')
    password = getpass.getpass(prompt='Type your password:')

    blacklist = try_get_list_from_file(blacklist_filepath)
    forbidden_list = try_get_list_from_file(forbidden_list_filepath)
    forbidden_list.append(username)

    print('password strength is:',
          calc_password_strength(password, blacklist, forbidden_list))
