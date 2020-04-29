import sys
from entry import Entry
from collection import Collection
import constants as c

'''
journal manager is a command line tool used to record and view
journal entires. it manages a file named 'journal.txt'. it is made by
joseph barsness.
'''


def main(sys_arguement=None):
    stored_entries.file_check()
    stored_entries.scan_journal()

    if sys_arguement is None:
        print(c.WELCOME_DISPLAY)
        welcome()

    # skip to command if launched using sys arguement
    elif sys_arguement == '-n':
        new_entry()
    elif sys_arguement == '-ng':
        new_entry('-ng')
    elif sys_arguement == '-nw':
        new_entry('-nw')
    elif sys_arguement == ('-e'):
        new_entry('-e')


def welcome():
    'always-on loop. controls function calls'
    while True:
        action = input(c.ACTION)

        if action == 'o' or action == 'new' or action == 'O':
            new_entry()
        elif action == 'p' or action == 'previous' or action == 'P':
            view_previous()
        elif action == 'h' or action == 'help' or action == 'H':
            print(f'\n{c.HELP}\n')
        elif action == 'refresh':
            stored_entries.wipe_journal()
        elif action == 'k' or action == 'quit' or action == 'K':
            print('\nty for visiting.')
            return


def new_entry(is_shortcut=None):
    'initiates a new entry. calls methods to open and record text box input'
    experience = str(input('\ntitle:\n'))

    if is_shortcut is None:
        new = Entry(experience)
    elif is_shortcut == '-ng':
        new = Entry(experience, '-ng')
    elif is_shortcut == '-nw':
        new = Entry(experience, '-nw')
    elif is_shortcut == '-e':
        new = Entry(experience, '-e')

    # refresh searchable list after every entry
    stored_entries.scan_journal()
    print(f'\nnew\n---\non {new.date} at {new.time}, '
          f'you wrote \'{new.thing_experienced}\'\n')


def view_previous():
    'prompts course of action on which entry to view'
    # refresh collection
    stored_entries.file_check()
    stored_entries.scan_journal()

    if len(stored_entries.collection) == 0:
        print('\nnone found. check location of journal.txt\n')
        return

    stored_entries.select()


stored_entries = Collection()
# check if a sys arguement is present
try:
    main(sys.argv[1])
except IndexError:
    main()

# TODO: remove entry function (both search and last)
# maybe auto quit after entry if using a sys arguement?s
