__author__ = 'Paddy'


def parse_settings(file_name):

    file_object = open(file_name, 'r')
    settings = {}

    for line in file_object:

        if line[0] == "#":
            # Skip this line because it is a comment
            pass

        else:

            n_line = line.strip('\n')
            n_line = n_line.split(' = ')

            try:
                settings[n_line[0]] = eval(n_line[1])

            except IndexError:
                pass

    return settings
