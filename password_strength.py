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
        help='Txt file with passwords blacklist, separated by new line',
        default='bl.txt'
    )
    parser.add_argument(
        '-fl',
        '--forbiddenlist_path',
        help='Txt file with abbreviations, birthdays and so on, '
             'separated by new line',
        default='fl.txt'
    )

    return parser.parse_args()


def is_special(char):
    all_normal_chars = string.ascii_letters + string.digits
    return char not in all_normal_chars


def calc_weakness_by_spec_chars(password):
    weakness_factor = 0
    spec_chars = [char for char in password if is_special(char)]
    if not spec_chars:
        weakness_factor += 2
    return weakness_factor


def calc_weakness_by_regex(password):
    upper_and_lower_chars = r'(?=[A-Z]*[a-z])(?=[a-z]*[A-Z])[a-zA-Z]'
    more_than_eight_chars_length = r'\S{8,}'
    digit_chars = r'\d'
    regex_list = [
        upper_and_lower_chars,
        more_than_eight_chars_length,
        digit_chars
    ]
    weakness_factor = 0
    for regex in regex_list:
        if not re.search(regex, password):
            weakness_factor += 2
    return weakness_factor


def calc_weakness_by_forbidden_list(password, forbidden_list):
    weakness_factor = 0
    for word in forbidden_list:
        if re.search(word, password):
            weakness_factor += 1
    return weakness_factor


def calc_password_strength(password, blacklist, forbidden_list):
    password_strength_min = 0
    password_strength_max = 10

    password_strength = password_strength_max

    if blacklist and password in blacklist:
        return password_strength_min

    password_strength -= calc_weakness_by_regex(password)
    password_strength -= calc_weakness_by_spec_chars(password)
    if forbidden_list:
        password_strength -= calc_weakness_by_forbidden_list(
            password, forbidden_list)

    return max(password_strength_min, password_strength)


if __name__ == '__main__':
    args = parse_args()
    blacklist_filepath = args.blacklist_path
    forbidden_list_filepath = args.forbiddenlist_path
    username = input('Type your username: ')
    password = getpass.getpass(prompt='Type your password:')

    blacklist = try_get_list_from_file(blacklist_filepath)
    forbidden_list = try_get_list_from_file(forbidden_list_filepath)

    if not blacklist:
        print('blacklist file not found')
    if not forbidden_list:
        print('forbidden list file not found')

    forbidden_list.append(username)

    print('password strength is:',
          calc_password_strength(password, blacklist, forbidden_list))
