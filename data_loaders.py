def try_get_list_from_file(filepath):
    try:
        return load_list_from_file(filepath)
    except FileNotFoundError:
        return []


def load_list_from_file(filepath):
    with open(filepath) as file_object:
        blacklist = file_object.readlines()
    return [line.strip() for line in blacklist]