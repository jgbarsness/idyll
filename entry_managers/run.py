from sys import argv
from entry_managers.full_entry import FullEntry
from entry_managers.title_entry import TitleEntry
from entry_managers.first_entry import FirstEntry
from entry_managers.second_entry import SecondEntry
from entry_managers.tag_entry import TagEntry
from collection.collection import Collection
from entry_managers.entrybox import TextBox
from mod_behaviors import command_strats, i_behavior
import constants.constants as c
from os import path, listdir
from pathlib import Path
from constants.file_handle import FileHandle
from gdrive import g_drive_auth

'''
idl is a command line tool used to manage text entries.
joseph barsness 2020
'''


def main(sys_arguement=None, title=None) -> None:
    'routes function calls'

    if sys_arguement is None:
        help_print()
        return

    # reduce calls to join
    joined_title = ' '.join(title)
    container = Collection(None)

    # call command if launched using sys arguement
    if sys_arguement == '-v':
        container.strategy = command_strats.ViewStrat()
        container.call_strat(joined_title)

    elif sys_arguement == '-wipe':
        if error_out("\ndefault entry file doesn't exist"):
            return
        FileHandle.wipe_collection()

    elif sys_arguement == '-wipe-all':
        if error_out('\nno folder to delete', c.FOLDER):
            return
        FileHandle.rm_folder()

    elif sys_arguement == '-b':
        if error_out("\ndefault entry file doesn't exist"):
            return
        FileHandle.backup_collection()

    elif sys_arguement == '-q':
        if error_out("\ndefault entry file doesn't exist"):
            return
        container.strategy = command_strats.QuickDeleteStrat()
        # if something was changed
        if container.call_strat(None):
            print('\n' + c.YELLOW + 'rewriting...' + c.END)
            FileHandle.refresh_collection(container.collection)
            print(c.YELLOW + 'done' + c.END)

    elif sys_arguement == '-del':
        if error_out("\ndefault entry file doesn't exist"):
            return
        # check for presence of entries. continue if so
        if (len(container.collection) != 0) and (len(joined_title) != 0):
            container.strategy = command_strats.DeleteModStrat()
            if container.call_strat(joined_title):
                print('\n' + c.YELLOW + 'rewriting...' + c.END)
                FileHandle.refresh_collection(container.collection)
                print(c.YELLOW + 'done' + c.END)
        # if no keyword is supplied to search with, show syntax
        else:
            print('\nnothing to show\nformat: idl -del [keyword]')

    elif sys_arguement == '-h' or sys_arguement == '-help':
        print(c.HELP)

    elif sys_arguement == '-load':
        FileHandle.load_from_backup()

    elif sys_arguement == '-config':
        if FileHandle.check_dir() is not False:
            # reset defaults
            FileHandle.gen_config('idl', c.DEFAULTS)
            print(c.YELLOW + '\nconfig updated as '
                  + c.PURPLE + path.abspath(c.FOLDER / 'idl.ini') + c.END)

    elif sys_arguement == '-t':
        container.strategy = command_strats.TSearchStrat()
        container.call_strat(joined_title)

    elif sys_arguement == '-s':
        if len(title) != 0:
            if FileHandle.check_dir() is not False:
                FileHandle.switch(joined_title)
        else:
            print("\nno name specified")
    elif sys_arguement == '-drive':
        g_drive_auth.upload()

    # create entry commands
    elif sys_arguement == '-n':
        call_entry('full', title, joined_title)
    elif sys_arguement == '-n1':
        call_entry('first', title, joined_title)
    elif sys_arguement == '-n2':
        call_entry('second', title, joined_title)
    elif sys_arguement == '-a':
        call_entry('tag', title, joined_title)
    elif sys_arguement == '-nt':
        call_entry('force', title, joined_title)
    else:
        call_entry('one_line', title, joined_title)


def call_entry(type_of: str, title: list, joined_title: str):
    'factory method to create entry'

    if FileHandle.check_dir() is False:
        return

    if type_of == 'full':
        if (len(title) != 0):
            # if title is supplied in same line
            new = FullEntry(joined_title)
        else:
            # run a full entry
            experience = str(input('\ntitle:\n'))
            new = FullEntry(experience)
    if type_of == 'first':
        if (len(title) != 0):
            new = FirstEntry(joined_title)
        else:
            experience = str(input('\ntitle:\n'))
            new = FirstEntry(experience)
    if type_of == 'second':
        if (len(title) != 0):
            new = SecondEntry(joined_title)

        else:
            experience = str(input('\ntitle:\n'))
            new = SecondEntry(experience)
    if type_of == 'tag':
        # must be at least two words long for both a tag and entry
        if len(title) > 1:
            # trim title to account for tag
            tag = title[0]
            end_title = ' '.join(title[1:])
            new = TagEntry(end_title, tag)
        else:
            print('\nno tag selected')
            return
    if type_of == 'force':
        # force a textbox entry
        new = TitleEntry(None, True)
    if type_of == 'one_line':
        new = TitleEntry(' '.join(argv[1:]))
    # call write / print on new object
    if new.print is True:
        new.write()
        new.printout()


def help_print():
    'prints out program info, including current active collections'

    # print out file locations
    if path.exists(c.DIR_NAME):
        if path.exists(c.COLLECTION_TITLE):
            print('current default: ' + c.PURPLE + path.abspath(c.COLLECTION_TITLE) + c.END)
        if path.exists(c.BACKUP_TITLE):
            print('backup: ' + c.PURPLE + path.abspath(c.BACKUP_TITLE) + c.END)

        # walk dir
        dirs = [f for f in listdir(c.DIR_NAME) if path.isdir(c.DIR_NAME / f)]
        pairs = []
        for f in dirs:
            files = [c for c in listdir(c.DIR_NAME / f) if c.endswith('.txt')]
            pairs.append(f + ': ' + ' '.join(files) + '\n')
        if len(pairs) > 0:
            print('collections:\n' + c.PURPLE + ''.join(pairs) + c.END)
    print(c.HEADER + c.HELP)


def error_out(message: str, location=c.COLLECTION_TITLE):
    'prints out message and returns true, else returns false if no error'

    if not FileHandle.file_verify(location):
        print(message)
        return True
    return False
