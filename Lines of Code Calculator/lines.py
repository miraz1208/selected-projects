"""
This program-

*** Expects exactly one command-line argument,
the name (or path) of a Python file,
and outputs the number of lines of code in that file,
excluding comments and blank lines.

*** If the user does not specify exactly one command-line argument,
or if the specified file's name does not end in '.py',
or if the specified file does not exist,
the program exits via sys.exit.
"""


import sys


def main():
    '''Checks all input, prints result accordingly'''
    length = len(sys.argv)
    checked_length = check_length(length)
    if checked_length:
        file_name = sys.argv[1]
        print(check_file(file_name))
    else:
        print(checked_length)


def check_length(command_line_length):
    '''Checks command line length'''
    if command_line_length < 2:
        sys.exit("Too few command-line arguments")
    elif command_line_length > 2:
        sys.exit("Too many command-line arguments")
    else:
        return True


def check_file(file_name):
    '''
    Checks line length of '.py' file.
    Returns length.
    Raises:
        FileNotFoundError:
            If file is not found, returns message.
    If not '.py' file, exits via sys.exit with message.
    '''
    count = 0
    if file_name.endswith(".py"):
        try:
            with open(file_name, "r", encoding="utf8") as file:
                lines = file.readlines()
                for _ in lines:
                    if _.lstrip().startswith("#"):
                        count += 0
                    elif _.isspace():
                        count += 0
                    else:
                        count += 1
                return count
        except FileNotFoundError:
            return "File does not exist"
    else:
        sys.exit("Not a python file")


if __name__ == "__main__":
    main()
