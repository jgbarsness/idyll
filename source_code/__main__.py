import sys
from entry import Entry
from collection import Collection
from entrybox import TextBox
import constants as c
import os

'''
jnl is a command line tool used to manage text entries.
joseph barsness 2020
'''


def main(sys_arguement=None, title=None):
    'routes function calls'

    if sys_arguement is None:
        # print out file locations
        if os.path.exists(c.JOURNAL_TITLE):
            print('collection: ' + c.PURPLE + os.path.abspath(c.JOURNAL_TITLE) + c.END)
        if os.path.exists(c.BACKUP_TITLE):
            print('backup: ' + c.PURPLE + os.path.abspath(c.BACKUP_TITLE) + c.END)
        print(c.HEADER + c.HELP)
        return
    # check files
    joined_title = ' '.join(title)

    # skip to command if launched using sys arguement
    if sys_arguement == '-v':
        if not stored_entries.file_verify():
            print("\nno entry file")
            return 
        stored_entries.scan_journal()
        # if there is a keyword to search with
        if (len(title) != 0):
            criteria = joined_title
            print('entries containing ' + '\'' + c.CYAN + criteria + c.END + '\':')
            stored_entries.show_keyword(joined_title)
        # if no keyword is present, print out entire journal
        else:
            # check for formatted entries
            if (len(stored_entries.collection) != 0):
                print('all entries:')
                stored_entries.print_entries(stored_entries.collection)
            else:
                # means that a file is present, but nothing could be parsed from it
                print('\ninvalid entry format')
    elif sys_arguement == '-wipe':
        if not stored_entries.file_verify():
            print("\nno entry file")
            return
        stored_entries.wipe_journal()
    elif sys_arguement == '-b':
        if not stored_entries.file_verify():
            print("\nno entry file")
            return
        stored_entries.backup_journal()
    elif sys_arguement == '-q':
        if not stored_entries.file_verify():
            print("\nno entry file")
            return
        stored_entries.quick_delete()
    elif sys_arguement == '-del':
        if not stored_entries.file_verify():
            print("\nno entry file")
            return
        stored_entries.scan_journal()
        # check for presence of entries. continue if so
        if (len(stored_entries.collection) != 0) and (len(title) != 0):
            stored_entries.delete_entry(joined_title)
        # if no keyword is supplied to search with, show syntax
        else:
            print('\nnothing to show\nformat: jnl -del [keyword]')
    elif sys_arguement == '-h' or sys_arguement == '-help':
        print(c.HELP)
    elif sys_arguement == '-load':
        stored_entries.load_from_backup()
    elif sys_arguement == '-config':
        if stored_entries.check_dir() == False:
            stored_entries.gen_config()
    elif sys_arguement == '-t':
        if not stored_entries.file_verify():
            print("\nno entry file")
            return
        stored_entries.scan_journal()
        if (len(stored_entries.collection) != 0) and (len(title) != 0):
            print('searching for tag ' + '\'' + c.CYAN + joined_title + c.END + '\':')
            stored_entries.show_keyword('(' + joined_title + ')')
        else:
            print('\nnothing to show\nformat: jnl -t [tag]')
    elif sys_arguement == '-s':
        if len(title) != 0:
            if stored_entries.check_dir() != False:
                stored_entries.switch(joined_title)
        else:
            print("\nno name specified")
    
    elif sys_arguement == '-n':
        if stored_entries.check_dir() == False:
            return
        # if a title is supplied in the same line
        if (len(title) != 0):
            # keep 'new' as a variable to possibly reference in later formatting decisions
            Entry(joined_title)
        else:
            # run a full entry
            experience = str(input('title:\n'))
            Entry(experience)
    elif sys_arguement == '-n1':
        if stored_entries.check_dir() == False:
            return
        if (len(title) != 0):
            Entry(joined_title, '-n1')
        else:
            experience = str(input('title:\n'))
            Entry(experience, '-n1')
    elif sys_arguement == '-n2':
        if stored_entries.check_dir() == False:
            return
        if (len(title) != 0):
            Entry(joined_title, '-n2')
        else:
            experience = str(input('title:\n'))
            Entry(experience, '-n2')
    elif sys_arguement == '-a':
        # must be at least two words long for both a tag and entry
        if len(title) > 1:
            if stored_entries.check_dir() == False:
                return
            # pass in tag as list to allow for formatting
            Entry(title, '-a')
        else:
            print('\nno tag selected')
    elif sys_arguement == '-nt':
        if stored_entries.check_dir() == False:
            return
        # force a textbox entry
        Entry(None, '-nt')
    else:
        if stored_entries.check_dir() == False:
            return
        # default to a one-lined title only entry
        Entry(' '.join(sys.argv[1:]), '-e')


if __name__ == '__main__':
    stored_entries = Collection()
    # check if a sys arguement is present
    try:
        main(sys.argv[1], sys.argv[2:])
    except IndexError:
        main()
