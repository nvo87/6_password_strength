import re
import argparse
import getpass
import string

from data_loaders import load_list_from_txt


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


def calc_password_strength(password, blacklist, forbidden_list):
    if password in blacklist:
        return 0

    password_strength = 10

    upper_and_lower_chars = r'(?=[A-Z]*[a-z])(?=[a-z]*[A-Z])[a-zA-Z]'
    more_than_eight_word_length = r'\S{8,}'
    numbers_chars = r'\d'
    regex_list = [
        upper_and_lower_chars,
        more_than_eight_word_length,
        numbers_chars
    ]

    for regex in regex_list:
        if not re.search(regex, password):
            password_strength -= 2

    for word in forbidden_list:
        if re.search(word, password):
            password_strength -= 1

    spec_chars = [char for char in password if is_special(char)]
    if not spec_chars:
        password_strength -= 2

    password_strength = max(0, password_strength)

    return password_strength


if __name__ == '__main__':
    blacklist_link = 'https://github.com/danielmiessler/' \
                     'SecLists/tree/master/Passwords'
    msg_about_pswrd_list = 'To check your password strength more correctly, ' \
                           'you should find blacklist and other forbidden ' \
                           'list by yourself. \n For example, ' \
                           'from here {}. \n ' \
                           'Type: -h for more info'.format(blacklist_link)
    args = parse_args()
    blacklist_filepath = args.blacklist_path
    forbidden_list_filepath = args.forbiddenlist_path
    username = input('Type your username: ')
    password = getpass.getpass(prompt='Type your password:')

    try:
        blacklist = load_list_from_txt(blacklist_filepath)
    except FileNotFoundError:
        print('Blacklist file is not found or its name is wrong. \n' +
              msg_about_pswrd_list)
        blacklist = []
    except TypeError:
        print(msg_about_pswrd_list)
        forbidden_list = []

    try:
        forbidden_list = load_list_from_txt(forbidden_list_filepath)
    except FileNotFoundError:
        print('Forbidden-list file is not found or its name is wrong. \n' +
              msg_about_pswrd_list)
        forbidden_list = []
    except TypeError:
        print(msg_about_pswrd_list)
        forbidden_list = []

    forbidden_list.append(username)

    print('password strength is:',
          calc_password_strength(password, blacklist, forbidden_list))
