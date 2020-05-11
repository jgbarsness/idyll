import sys
from entry import Entry
from collection import Collection
import constants as c

'''
journal mngr is a command line tool used to manage text entries
it is made by joseph barsness

copyright 2020, joseph barsness. all rights reserved.
'''


def main(sys_arguement=None, title=None):
    # check files
    stored_entries.file_check()
    stored_entries.scan_journal()

    if sys_arguement is None:
        print(c.WELCOME_DISPLAY)
        welcome()

    # skip to command if launched using sys arguement
    elif sys_arguement == '-n':
        if len(title) != 0:
            new_entry(None, ' '.join(title))
        else:
            new_entry()
    elif sys_arguement == '-ng':
        if len(title) != 0:
            new_entry('-ng', ' '.join(title))
        else:
            new_entry('-ng')
    elif sys_arguement == '-nw':
        if len(title) != 0:
            new_entry('-nw', ' '.join(title))
        else:
            new_entry('-nw')
    elif sys_arguement == '-e':
        if len(title) != 0:
            new_entry('-e', ' '.join(title))
        else:
            new_entry('-e')
    elif sys_arguement == '-v':
        stored_entries.display_journal()
    elif sys_arguement == '-wipe':
        stored_entries.wipe_journal()
    elif sys_arguement == '-b':
        stored_entries.backup_journal()


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
        elif action == 'wipe':
            stored_entries.wipe_journal()
        elif action == 'backup':
            stored_entries.backup_journal()
        elif action == 'load':
            stored_entries.load_from_backup()
        elif action == 'config':
            stored_entries.gen_config()
        elif action == 'k' or action == 'quit' or action == 'K':
            print('\nclosing')
            return


def new_entry(is_shortcut=None, entry_title=None):
    'initiates a new entry. calls methods to open and record text box input'

    if is_shortcut is None:
        if entry_title is not None:
            new = Entry(entry_title)
        else:
            experience = str(input('\ntitle:\n'))
            new = Entry(experience)
    elif is_shortcut == '-ng':
        if entry_title is not None:
            new = Entry(entry_title, '-ng')
            new.thing_experienced == sys.argv[2:]
        else:
            experience = str(input('\ntitle:\n'))
            new = Entry(experience, '-ng')
    elif is_shortcut == '-nw':
        if entry_title is not None:
            new = Entry(entry_title, '-nw')
            new.thing_experienced == sys.argv[2:]
        else:
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
        print('\nnone found. check location of journal\n')
        return

    stored_entries.select()


stored_entries = Collection()
# check if a sys arguement is present
try:
    main(sys.argv[1], sys.argv[2:])
except IndexError:
    main()
