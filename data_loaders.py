def load_list_from_txt(filepath):
    with open(filepath) as file_object:
        blacklist = file_object.readlines()
    return [item.strip() for item in blacklist]