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
        print(c.HEADER + c.HELP)
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
    elif sys_arguement == '-n1':
        if len(title) != 0:
            new_entry('-n1', ' '.join(title))
        else:
            new_entry('-n1')
    elif sys_arguement == '-n2':
        if len(title) != 0:
            new_entry('-n2', ' '.join(title))
        else:
            new_entry('-n2')
    elif sys_arguement == '-e':
        if len(title) != 0:
            new_entry('-e', ' '.join(title))
        else:
            new_entry('-e')
    elif sys_arguement == '-v':
        if (len(title) != 0):
            stored_entries.show_keyword(' '.join(title))
        else:
            stored_entries.display_journal()
    elif sys_arguement == '-wipe':
        stored_entries.wipe_journal()
    elif sys_arguement == '-b':
        stored_entries.backup_journal()
    elif sys_arguement == '-q':
        stored_entries.quick_delete()
    elif sys_arguement == '-del':
        # check for presence of file. continue if so
        if check() is False and (len(title) != 0):
            stored_entries.delete_entry(' '.join(title))
        else:
            print('\nnothing found. format: jnl -del [keyword]\n')
    elif sys_arguement == '-h' or sys_arguement == '-help':
        print(c.HELP)
    elif sys_arguement == '-load':
        stored_entries.load_from_backup()
    elif sys_arguement == '-config':
        stored_entries.gen_config()
    elif sys_arguement == '-t':
        if check() is False and (len(title) != 0):
            stored_entries.show_keyword('(' + ' '.join(title) + ')')
        else:
            print('\nnothing found. format: jnl -t [keyword]\n')
    elif sys_arguement == '-a':
        # must be at least two words long for both a tag and entry
        if len(title) > 1:
            new_entry('-a', title)
        else:
            print('\nno tag selected\n')
    else:
        # default to a one-lined title only entry
        new_entry('-e', ' '.join(sys.argv[1:]))


def new_entry(is_shortcut=None, entry_title=None):
    'initiates a new entry. calls methods to open and record text box input'

    if is_shortcut is None:
        if entry_title is not None:
            new = Entry(entry_title)
        else:
            experience = str(input('\ntitle:\n'))
            new = Entry(experience)
    elif is_shortcut == '-n1':
        if entry_title is not None:
            new = Entry(entry_title, '-n1')
        else:
            experience = str(input('\ntitle:\n'))
            new = Entry(experience, '-n1')
    elif is_shortcut == '-n2':
        if entry_title is not None:
            new = Entry(entry_title, '-n2')
        else:
            experience = str(input('\ntitle:\n'))
            new = Entry(experience, '-n2')
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
    # print out entry info + title
    print(f'\nnew\n---\non {new.date} at {new.time}, '
          f'you wrote \'{new.title}\'\n')


def check():
    'checks for entry presence. returns true if empty file'

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
