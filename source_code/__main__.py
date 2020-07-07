import sys
from entry import Entry
from collection import Collection
from entrybox import TextBox
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
    joined_title = ' '.join(title)
    stored_entries.file_check()
    stored_entries.scan_journal()

    # skip to command if launched using sys arguement
    if sys_arguement == '-v':
        if not_null(title):
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

    elif sys_arguement == '-n':
        if not_null(title):
            new = Entry(joined_title)
        else:
            experience = str(input('\ntitle:\n'))
            new = Entry(experience)
        printout(new.date, new.time, new.title)
    elif sys_arguement == '-n1':
        if not_null(title):
            new = Entry(joined_title, '-n1')
        else:
            experience = str(input('\ntitle:\n'))
            new = Entry(experience, '-n1')
        printout(new.date, new.time, new.title)
    elif sys_arguement == '-n2':
        if not_null(title):
            new = Entry(joined_title, '-n2')
        else:
            experience = str(input('\ntitle:\n'))
            new = Entry(experience, '-n2')
        printout(new.date, new.time, new.title)
    elif sys_arguement == '-a':
        # must be at least two words long for both a tag and entry
        if len(title) > 1:
            # pass in tag as list to allow for formatting
            new = Entry(title, '-a')
            printout(new.date, new.time, new.title)
        else:
            print('\nno tag selected\n')
    elif sys_arguement == '-nt':
        new = Entry(None, '-nt')
        printout(new.date, new.time, new.title)
    else:
        # default to a one-lined title only entry
        new = Entry(' '.join(sys.argv[1:]), '-e')
        printout(new.date, new.time, new.title)


def printout(date, time, title):
    'prints out the entry'

    # refresh searchable list after every entry
    stored_entries.scan_journal()
    # print out entry info + title
    print(f'\nnew\n---\non {date} at {time}, '
          f'you wrote \'{title}\'\n')


def not_null(title):
    'checks for null'

    return (len(title) != 0)


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
