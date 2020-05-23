import sys
from entry import Entry
from collection import Collection
import constants as c

'''
journal mngr is a command line tool used to manage text entries.
joseph barsness 2020
'''


def main(sys_arguement=None, title=None):
    'routes function calls'
    if sys_arguement is None:
        print(c.HELP)
        # disallow running without sys
        return
    # check files
    stored_entries.file_check()
    stored_entries.scan_journal()

    # skip to command if launched using sys arguement
    if sys_arguement == '-n':
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
    elif sys_arguement == '-q':
        stored_entries.quick_delete()
    elif sys_arguement == '-del':
        # check for presence of file. continue if so
        if check() is False:
            criteria = input('\nenter a phrase to search for:\n')
            stored_entries.delete_entry(criteria)
        else:
            print('\nno entries.\n')
    elif sys_arguement == '-h' or sys_arguement == '-help':
        print(f'\n{c.HELP}\n')
    elif sys_arguement == '-load':
        stored_entries.load_from_backup()
    elif sys_arguement == '-config':
        stored_entries.gen_config()
    elif sys_arguement == '-k':
        is_entries = check()
        if is_entries is False and (len(title) != 0):
            stored_entries.show_keyword(' '.join(title))
        else:
            print('\nformat: journal -k [keyword]\n')
    elif sys_arguement == '-t':
        is_entries = check()
        if is_entries is False and (len(title) != 0):
            stored_entries.show_keyword('(' + ' '.join(title) + ')')
        else:
            print('\nformat: journal -t [keyword]\n')
    elif sys_arguement == '-a':
        # must be at least two words long for both a tag and entry
        if len(title) > 1:
            new_entry('-a', title)
        else:
            print('\nno tag selected\n')


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
        else:
            experience = str(input('\ntitle:\n'))
            new = Entry(experience, '-ng')
    elif is_shortcut == '-nw':
        if entry_title is not None:
            new = Entry(entry_title, '-nw')
        else:
            experience = str(input('\ntitle:\n'))
            new = Entry(experience, '-nw')
    elif is_shortcut == '-e':
        if entry_title is not None:
            new = Entry(entry_title, '-e')
        else:
            experience = str(input('\ntitle:\n'))
            new = Entry(experience, '-e')
    elif is_shortcut == '-a':
        new = Entry(entry_title, '-a')

    # refresh searchable list after every entry
    stored_entries.scan_journal()
    print(f'\nnew\n---\non {new.date} at {new.time}, '
          f'you wrote \'{new.thing_experienced}\'\n')


def check():
    'checks for entry presence. returns true if empty file'
    # refresh collection

    if len(stored_entries.collection) == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    stored_entries = Collection()
    # check if a sys arguement is present
    try:
        main(sys.argv[1], sys.argv[2:])
    except IndexError:
        main()
