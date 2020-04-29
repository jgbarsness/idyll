import sys
from entry import Entry
from collection import Collection
import constants as c

'''
journal manager is a command line tool used to record and view
journal entires. it manages a file named 'journal.txt'. it is made by
joseph barsness.
'''


def main(sys_arguement=None, title=None):
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
    elif sys_arguement == '-e':
        if len(title) != 0:
            new_entry('-e', ' '.join(title))
        else:
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
            print('\nclosing')
            return


def new_entry(is_shortcut=None, entry_title=None):
    'initiates a new entry. calls methods to open and record text box input'

    if is_shortcut is None:
        experience = str(input('\ntitle:\n'))
        new = Entry(experience)
    elif is_shortcut == '-ng':
        experience = str(input('\ntitle:\n'))
        new = Entry(experience, '-ng')
    elif is_shortcut == '-nw':
        experience = str(input('\ntitle:\n'))
        new = Entry(experience, '-nw')
    elif is_shortcut == '-e':
        if entry_title is not None:
            new = Entry(entry_title, '-e')
            new.thing_experienced == sys.argv[2:]
        else:
            experience = str(input('\ntitle:\n'))
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
    main(sys.argv[1], sys.argv[2:])
except IndexError:
    main()

# TODO: remove entry function (both search and last)
# keyword print out all matches instead of random
