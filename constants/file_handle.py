import constants.constants as c
import os
from shutil import copy, rmtree
from pathlib import Path
import configparser
import stat


class FileHandle:
    'utility class. file handling logic for collection data'

    @staticmethod
    def file_verify(f=c.COLLECTION_TITLE):
        'checks for presence of entry file'

        return os.path.exists(f)

    @staticmethod
    def backup_collection():
        'creates a backup collection file'

        # uses 'copy' to preserve permissions
        # in case future update relies on permission at close
        try:
            copy(c.COLLECTION_TITLE, c.BACKUP_TITLE)
            print(c.YELLOW + '\nbackup created as ' + c.PURPLE + os.path.abspath(c.BACKUP_TITLE)+ c.END)
            return
        except PermissionError:
            # verify desired behavior
            choice = input('\nbackup detected. overwrite? y/n\n')
            if choice == 'y':
                pass
            else:
                print('\nno update made')
                return

        try:
            os.remove(c.BACKUP_TITLE)
            # retain a backup copy
            copy(c.COLLECTION_TITLE, c.BACKUP_TITLE)
            print(c.YELLOW + '\nbackup updated as ' + c.PURPLE + os.path.abspath(c.BACKUP_TITLE) + c.END)
        except FileNotFoundError:
            # user machine removed file themselves after running program
            print(c.RED + '\nerror: bad backup' + c.END)
            raise

    @staticmethod
    def wipe_all():
        'deletes entire contents folder'

        answer = input('\ndelete every collection in this directory? y/n\n')
        if answer != 'y':
            print('\nnothing deleted')
            return
        print(c.YELLOW + 'deleting all...' + c.END)
        try:
            rmtree(c.FOLDER)
        except Exception:
            print(c.RED + '\nsomething went wrong\n' + c.END)
            raise
        print(c.YELLOW + 'everything deleted' + c.END)

    @staticmethod
    def check_dir(dire=c.FOLDER):
        'checks for presence of a directory, and creates if not found'

        if not os.path.exists(dire):
            verify = input("\nno collection directory here. create? y/n\n")
            if verify != "y":
                print("\nno directory created")
                return False
            os.makedirs(dire)
            return True

    @staticmethod
    def switch(new):
        'sets a new name for default collection'

        # if file doesn't exist, verify
        name = new + '.txt'
        path = c.FOLDER / name
        if FileHandle.file_verify(path) == False:
            verify = input("\nno collection by that name. set as default collection? y/n\n")
            if verify != 'y':
                print("\nnothing modified")
                return

        # preserve modifications
        keep = [c.END_MARKER, c.DATESTAMP_UNDERLINE, c.FIRST_MARKER, c.SECOND_MARKER, c.USE_TEXTBOX]
        print("\nsetting " + c.PURPLE + new + ".txt" + c.END + "...")
        FileHandle.gen_config(new, keep)
        print(c.PURPLE + new + ".txt" + c.END + " is new default collection")

    @staticmethod
    def gen_config(active='idl', deff=c.DEFAULTS):
        'generate config file in pwd'

        config = configparser.ConfigParser()
        config['DEFAULT'] = {'END_MARKER': deff[0],
                             'DATESTAMP_UNDERLINE': deff[1],
                             'COLLECTION_TITLE': active,
                             'BACKUP_TITLE': 'b_' + active,
                             'FIRST_MARKER': deff[2],
                             'SECOND_MARKER': deff[3],
                             'USE_TEXTBOX': deff[4]}

        try:
            configfile = open(c.FOLDER / 'idl.ini', 'w')
        except FileNotFoundError:
            print(c.RED + 'no file to modify - something went wrong' + c.END)
            raise
        config.write(configfile)
        configfile.write(c.CONFIG_MESSAGE)
        configfile.close()

    @staticmethod
    def load_from_backup():
        'makes backup the running document'

        if not os.path.exists(c.BACKUP_TITLE):
            print('\nno backup found')
            return

        selection = input('\nrestore from backup? y/n\n')
        if selection == 'y':
            # make sure correct collection is retained
            try:
                os.remove(c.COLLECTION_TITLE)
            except FileNotFoundError:
                print(c.PURPLE + "creating new file, retaining backup..." + c.END)

            print(c.YELLOW + '\nrestoring...' + c.END)
            # backup -> running file
            try:
                os.rename(c.BACKUP_TITLE, c.COLLECTION_TITLE)
                # retain a copy
                copy(c.COLLECTION_TITLE, c.BACKUP_TITLE)
                print(c.YELLOW + 'restored from ' + c.PURPLE + os.path.abspath(c.BACKUP_TITLE) + c.END)
            except FileNotFoundError:
                # user machine removed file themselves after running program
                print(c.RED + '\nerror: bad backup' + c.END)
                raise

        else:
            print('\nload from backup cancelled')
            return

    @staticmethod
    def wipe_collection():
        'completely delete collection'

        selection = input('\ndelete default collection? y/n\n')

        if selection == 'y':
            try:
                print(c.YELLOW + '\ndeleting...' + c.END)
                os.remove(c.COLLECTION_TITLE)
                print(c.PURPLE + os.path.abspath(c.COLLECTION_TITLE) + c.YELLOW + ' deleted' + c.END)
            except FileNotFoundError:
                # user machine removed file themselves after running program
                print(c.RED + '\nerror: file doesn\'t exist' + c.END)
                raise
        else:
            print('\nfile preserved')
            return

    @staticmethod
    def refresh_collection(container):
        'after deletion of entry, re-write collection to reflect changes'

        try :
            # make collection writeable
            os.chmod(c.COLLECTION_TITLE, stat.S_IRWXU)
            refresh = open(c.COLLECTION_TITLE, 'w')
        except FileNotFoundError:
            print(c.RED + 'no file to modify - something went wrong' + c.END)
            raise

        for entry in container:
            refresh.write(entry)
            refresh.write(c.END_MARKER + '\n\n')

        os.chmod(c.COLLECTION_TITLE, stat.S_IREAD)
        refresh.close()
