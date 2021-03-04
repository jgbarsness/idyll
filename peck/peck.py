from sys import argv, path
from peck.file_handle import FileHandle
from peck.title_entry import TitleEntry
from peck.first_entry import FirstEntry
from peck.second_entry import SecondEntry
from peck.tag_entry import TagEntry
from peck.full_entry import FullEntry
from peck.collection import Collection
import peck.modify_strats
import peck.view_strats
import peck.info_and_paths as c
import peck.commands as cmd
import peck.errors as e
from os import path, listdir
from pathlib import Path
# from gdrive import g_drive_auth

'''
peck is a command line tool used to manage text entries.
joseph barsness 2020
'''


def main(sys_arguement=None, title=None) -> None:
    'routes function calls'

    if sys_arguement is None:
        print(c.VERSION + '\n' + c.HELP)
        return

    # reduce calls to join
    joined_title = ' '.join(title)
    # collection using parsed file path, or default
    container = Collection(None, c.COLLECTION_TITLE)

    # call command if launched using sys arguement
    if sys_arguement == cmd.VIEW:
        container.strategy = peck.view_strats.ViewStrat()
        container.call_strat(joined_title)

    elif sys_arguement == cmd.VIEW_FILE:
        # construct the file name with the passed name + txt extension
        add_exten = title[0] + '.txt'
        # create posix path out of current folder + name
        pos_title = c.FOLDER / add_exten
        if path.isfile(pos_title):
            container = Collection(peck.view_strats.ViewStrat(), pos_title)
            container.call_strat(''.join(title[1:]))
        else:
            print(e.INVALID_FILE_VIEW)

    elif sys_arguement == cmd.DATESEARCH:
        container.strategy = peck.view_strats.DateSearch()
        container.call_strat(joined_title)

    elif sys_arguement == cmd.WIPE:
        if error_out(e.NONEXIST_ERROR):
            return
        FileHandle.wipe_collection()

    elif sys_arguement == cmd.WIPE_ALL:
        if error_out(e.WIPE_ALL_ERROR, c.FOLDER):
            return
        selection = selection = input('\ndelete all collections referencing this directory? y/n \n')
        if selection == 'y':
            FileHandle.rm_folder()
        else:
            print('\nfolder preserved')

    elif sys_arguement == cmd.BACKUP:
        if error_out(e.NONEXIST_ERROR):
            return
        FileHandle.backup_collection()

    elif sys_arguement == cmd.QUICK_DELETE:
        if error_out(e.NONEXIST_ERROR):
            return
        container.strategy = peck.modify_strats.QuickDeleteStrat()
        # if something was changed
        if container.call_strat(None):
            print('\n' + c.YELLOW + 'rewriting...' + c.END)
            FileHandle.refresh_collection(container.collection)
            print(c.YELLOW + 'done' + c.END)

    elif sys_arguement == cmd.DELETE:
        if error_out(e.NONEXIST_ERROR):
            return
        # check for presence of entries. continue if so
        if (len(container.collection) != 0) and (len(joined_title) != 0):
            container.strategy = modify_strats.DeleteModStrat()
            if container.call_strat(joined_title):
                print('\n' + c.YELLOW + 'rewriting...' + c.END)
                FileHandle.refresh_collection(container.collection)
                print(c.YELLOW + 'done' + c.END)
        # if no keyword is supplied to search with, show syntax
        else:
            print(e.DELETE_ERROR)

    elif sys_arguement == cmd.LIST:
        directory_print()

    elif sys_arguement == cmd.LOAD:
        FileHandle.load_from_backup()

    elif sys_arguement == cmd.CONFIG:
        if FileHandle.check_dir() is not False:
            # reset defaults
            FileHandle.gen_config('pck', c.DEFAULTS)
            print('\nconfig updated as '
                  + c.PURPLE + path.abspath(c.FOLDER / 'pck.ini') + c.END)

    elif sys_arguement == cmd.TAG_SEARCH:
        container.strategy = view_strats.TSearchStrat()
        container.call_strat(joined_title)

    elif sys_arguement == cmd.SWITCH:
        if len(title) != 0:
            if FileHandle.check_dir() is not False:
                FileHandle.switch(joined_title)
        else:
            print(e.SWITCH_ERROR)
    
    # TODO: implement drive functionality in build
    # elif sys_arguement == cmd.G_DRIVE:
        # g_drive_auth.upload()
    

    # create entry commands
    elif sys_arguement == cmd.NEW:
        call_entry('full', title)
    elif sys_arguement == cmd.NEW_FIRST:
        call_entry('first', title)
    elif sys_arguement == cmd.NEW_SECOND:
        call_entry('second', title)
    elif sys_arguement == cmd.TAG:
        call_entry('tag', title)
    elif sys_arguement == cmd.FORCE_TEXTBOX:
        call_entry('force', title)
    else:
        call_entry('one_line', title)


def call_entry(type_of: str, title: list):
    'factory method to create entry'

    joined_title = ''.join(title)

    if FileHandle.check_dir() is False:
        return

    view_title = "\ntitle:\n"
    if type_of == 'full':
        if (len(title) != 0):
            # if title is supplied in same line
            new = FullEntry(joined_title)
        else:
            # run a full entry
            experience = str(input(view_title))
            new = FullEntry(experience)
    if type_of == 'first':
        if (len(title) != 0):
            new = FirstEntry(joined_title)
        else:
            experience = str(input(view_title))
            new = FirstEntry(experience)
    if type_of == 'second':
        if (len(title) != 0):
            new = SecondEntry(joined_title)

        else:
            experience = str(input(view_title))
            new = SecondEntry(experience)
    if type_of == 'tag':
        # must be at least two words long for both a tag and entry
        if len(title) > 1:
            # trim title to account for tag
            tag = title[0]
            end_title = ' '.join(title[1:])
            new = TagEntry(end_title, tag)
        else:
            print(e.TAG_ERROR)
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


def directory_print():
    'prints out current active collections'

    headers = []
    # print out file locations
    if path.exists(c.DIR_NAME):
        if path.exists(c.COLLECTION_TITLE):
            headers.append(c.PURPLE + 'current default: ' +
                           c.END + path.abspath(c.COLLECTION_TITLE))
        if path.exists(c.BACKUP_TITLE):
            headers.append(c.PURPLE + 'backup: ' + c.END +
                           path.abspath(c.BACKUP_TITLE))

        # walk dir
        dirs = [f for f in listdir(c.DIR_NAME) if path.isdir(c.DIR_NAME / f)]
        pairs = []
        inactive = []
        for f in dirs:
            # search for note files
            files = [c for c in listdir(c.DIR_NAME / f) if c.endswith('.txt')]
            if len(files) > 0:
                pairs.append(f + ': ' + ' | '.join(files))
            # if none are found coupled with a folder, mark the folder as inactive
            else:
                inactive.append(f)
        if len(pairs) > 0:
            headers.append(c.PURPLE + 'directories in use:\n' + c.END
                           + '\n'.join(pairs))
        if len(inactive) > 0:
            headers.append(c.PURPLE + 'inactive directories:\n' + c.END
                           + '\n'.join(inactive))

        print('\n\n'.join(headers))


def error_out(message: str, location=c.COLLECTION_TITLE):
    'prints out message and returns true, else returns false if no error'

    if not FileHandle.file_verify(location):
        print(message)
        return True
    return False


def driver():
    # check if a sys arguement is present
    try:
        main(argv[1], argv[2:])
    except IndexError:
        main()