def try_get_list_from_file(filepath):
    blacklist_link = 'https://github.com/danielmiessler/' \
                     'SecLists/tree/master/Passwords'
    msg_about_pswrd_list = 'To check your password strength more correctly, ' \
                           'you should find blacklist and other forbidden ' \
                           'list by yourself. \n For example, from here {}. \n ' \
                           'Type: -h for more info'.format(blacklist_link)
    try:
        return load_list_from_file(filepath)
    except FileNotFoundError:
        print('{} is not found or its name is wrong. \n'.format(filepath) +
              msg_about_pswrd_list)
        return []
    except TypeError:
        print(msg_about_pswrd_list)
        return []


def load_list_from_file(filepath):
    with open(filepath) as file_object:
        blacklist = file_object.readlines()
    return [line.strip() for line in blacklist]