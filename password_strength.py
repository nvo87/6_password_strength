import re
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description='This script calc the strength of your password.')
    parser.add_argument('password', help='type your password', type=str)

    return parser.parse_args()


def get_password_strength(password):
    ''' Main idea is that your password has already max strength = 10.
        But if it hasn't both upper and lowercase, numbers, or it length less than 8,
        strength will be weakened for 2 points per each factor respectivily.
        If your password contains words from popular data lists (userdata, dates, abbreveations),
        total strength decrease by 1 point for each overlap.
    '''
    blacklist = ['11111111', 'qwerty', '12345678']

    if password in blacklist:
        return 0

    # connect your forbidden lists below.
    userdata = ['slava', '02101987']
    abbreviations = ['bmw', 'lsd', 'nestle']
    spec_numbers = ['09051945', '0911']
    forbidden_list = userdata + abbreviations + spec_numbers    

    has_upper_and_lower_regex = r'(?=[A-Z]*[a-z])(?=[a-z]*[A-Z])[a-zA-Z]'
    more_than_eight = r'\S{8,}'
    has_numbers_regex = r'\d'
    has_spec_char = r'[@#$]'
    regex_list = [
        has_upper_and_lower_regex,
        more_than_eight,
        has_numbers_regex,
        has_spec_char
    ]

    password_strength = 10

    for regex in regex_list:
        if not re.search(regex, password):
            password_strength -= 2

    for word in forbidden_list:
        if re.search(word, password):
            password_strength -= 1

    password_strength = 0 if password_strength < 0 else password_strength

    return password_strength
        

if __name__ == '__main__':
    args = parse_args()
    password = args.password

    print('password strength is:', get_password_strength(password))

