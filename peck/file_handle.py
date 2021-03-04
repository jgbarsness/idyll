import peck.info_and_paths as c
from os import path, remove, makedirs, rename, chmod, listdir
from shutil import copy, rmtree
from pathlib import Path
from configparser import ConfigParser
from stat import S_IRWXU, S_IREAD


class FileHandle:
    'utility class. file handling logic for collection data'

    @staticmethod
    def file_verify(f=c.COLLECTION_TITLE):
        'checks for presence of entry file'

        return path.exists(f)

    @staticmethod
    def backup_collection():
        'creates a backup collection file'

        # uses 'copy' to preserve permissions
        # in case future update relies on permission at close
        if not path.exists(c.BACKUP_TITLE):
            copy(c.COLLECTION_TITLE, c.BACKUP_TITLE)
            print('\nbackup created as ' + c.PURPLE + path.abspath(c.BACKUP_TITLE)+ c.END)
            return
        else:
            # verify desired behavior
            choice = input('\nbackup detected. overwrite? y/n\n')
            if choice != 'y':
                print('\nno update made')
                return

        try:
            remove(c.BACKUP_TITLE)
            # retain a backup copy
            copy(c.COLLECTION_TITLE, c.BACKUP_TITLE)
            print('\nbackup updated as ' + c.PURPLE + path.abspath(c.BACKUP_TITLE) + c.END)
        except FileNotFoundError:
            # user machine removed file themselves after running program
            print(c.RED + '\nerror: old backup already removed' + c.END)
            return

    @staticmethod
    def check_dir(dire=c.FOLDER):
        'checks for presence of a directory, and creates if not found'

        if not path.exists(dire):
            verify = input("\nno directory folder. create? y/n\n")
            if verify != "y":
                print("\nno directory created")
                return False
            makedirs(dire)
            return True

    @staticmethod
    def switch(new):
        'sets a new name for default collection'

        # if file doesn't exist, verify
        name = new + '.txt'
        path = c.FOLDER / name
        if FileHandle.file_verify(path) == False:
            verify = input("\nno collection by that name in this directory. set as default collection? y/n\n")
            if verify != 'y':
                print("\nnothing modified")
                return

        # preserve modifications
        keep = [c.END_MARKER, c.DATESTAMP_UNDERLINE, c.FIRST_MARKER, c.SECOND_MARKER, c.USE_TEXTBOX]
        print("\nsetting " + new + ".txt" + "...")
        FileHandle.gen_config(new, keep)
        print(new + ".txt" + " is the new default collection")

    @staticmethod
    def gen_config(active='pck', deff: list=c.DEFAULTS):
        'generate config file in pwd'

        config = ConfigParser()
        config['DEFAULT'] = {'END_MARKER': deff[0],
                             'DATESTAMP_UNDERLINE': deff[1],
                             'COLLECTION_TITLE': active,
                             'BACKUP_TITLE': 'b_' + active,
                             'FIRST_MARKER': deff[2],
                             'SECOND_MARKER': deff[3],
                             'USE_TEXTBOX': deff[4]}

        try:
            configfile = open(c.FOLDER / 'pck.ini', 'w')
        except FileNotFoundError:
            print(c.RED + 'error: no file to modify' + c.END)
            return
        config.write(configfile)
        configfile.write(c.CONFIG_MESSAGE)
        configfile.close()

    @staticmethod
    def load_from_backup():
        'makes backup the running document'

        if not path.exists(c.BACKUP_TITLE):
            print('\nno backup found')
            return

        selection = input('\nrestore from backup? y/n\n')
        if selection == 'y':
            # make sure correct collection is retained
            try:
                remove(c.COLLECTION_TITLE)
            except FileNotFoundError:
                print("creating new file, retaining backup...")

            print(c.YELLOW + '\nrestoring...' + c.END)
            # backup -> running file
            try:
                rename(c.BACKUP_TITLE, c.COLLECTION_TITLE)
                # retain a copy
                copy(c.COLLECTION_TITLE, c.BACKUP_TITLE)
                print('restored from ' + path.abspath(c.BACKUP_TITLE))
            except FileNotFoundError:
                # user machine removed file themselves after running program
                print(c.RED + '\nerror: no backup found' + c.END)
                return

        else:
            print('\nload from backup cancelled')
            return

    @staticmethod
    def wipe_collection():
        'completely delete default collection'

        selection = input('\ndelete current default collection? y/n\n')

        if selection == 'y':
            try:
                print(c.YELLOW + '\ndeleting...' + c.END)
                remove(c.COLLECTION_TITLE)
                print(path.abspath(c.COLLECTION_TITLE) + c.YELLOW + ' deleted' + c.END)
            except FileNotFoundError:
                # user machine removed file themselves after running program
                print(c.RED + '\nerror: file doesn\'t exist' + c.END)
                return

            if not FileHandle.validate_subdirectory():
                selection = input('\nlast collection file in directory has been deleted. delete directory, including config file? y/n\n')
                if selection == 'y':
                    FileHandle.rm_folder()
                else:
                    print('\ndirectory retained')
                    return
            
        else:
            print('\nfile preserved')
            return

    @staticmethod 
    def validate_subdirectory():
        'checks to see if the current subdirectory has an active text file(s) in it'

        files = [c for c in listdir(c.FOLDER) if c.endswith('.txt')]
        return len(files) > 0

    @staticmethod
    def rm_folder():
        'deletes entire directory folder'

        try:
            print(c.YELLOW + '\ndeleting...' + c.END)
            rmtree(c.FOLDER)
            print(str(c.FOLDER) + c.YELLOW + ' deleted' + c.END)
        except FileNotFoundError:
            print(c.RED + '\nerror: folder doesn\'t exist' + c.END)
            return

    @staticmethod
    def refresh_collection(container):
        're-write collection to reflect changes'

        try:
            # make collection writeable
            chmod(c.COLLECTION_TITLE, S_IRWXU)
            refresh = open(c.COLLECTION_TITLE, 'w')
        except FileNotFoundError:
            print(c.RED + 'error: file not found' + c.END)
            return

        for entry in container:
            refresh.write(entry)
            refresh.write(c.END_MARKER + '\n\n')

        chmod(c.COLLECTION_TITLE, S_IREAD)
        refresh.close()
