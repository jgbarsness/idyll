import constants as c
import random
import re
import os
import stat
from shutil import copy, rmtree
from pathlib import Path
import configparser


class Collection:
    'a collection of entries. manages file storage and display'
    
    def __init__(self):
        self.collection = []

    def return_thing(self, key):
        'returns a list of all entries containing a keywork'

        # search for instances of keyword
        entry = [elmnt for elmnt in self.collection if key in elmnt]

        return entry

    def show_keyword(self, key):
        'shows entries if keyword matches'

        entry = self.return_thing(key)
        if (len(entry) == 0):
            print('\nnothing to show')

        # if function can continue, print out entry
        self.print_entries(entry)
        return entry

    def print_entries(self, container):
        'used to print out things entries after search is ran'

        for thing in container:
            print('\n' + thing + c.SEPERATOR)

    def delete_entry(self, entry):
        'bulk or single delete entries'

        delete = self.return_thing(entry)
        # if nothing is returned by previous call, end
        if (len(delete) == 0):
            print('\nnothing to delete containing ' 
                  + '\'' + c.CYAN + entry + c.END + '\'')
            return

        # if function can continue, print out entry
        print('to be deleted, containing ' + '\'' + c.CYAN + entry + c.END + '\':')
        self.print_entries(delete)

        choice = input('\ndelete? y/n\n')

        if choice == 'y':
            print(c.YELLOW + '\ndeleting entries...' + c.END)

            # find all occurances
            for things in delete:
                # remove them
                self.collection.remove(things)
            self.refresh_collection()
            print(c.YELLOW + 'entries deleted' + c.END)

        else:
            print('\nentries preserved')
            return

    def scan_collection(self, fpath=c.collection_TITLE):
        'returns collection list of collection entries'

        os.chmod(fpath, stat.S_IRWXU)
        try:
            collection = open(fpath, 'r')
        except FileNotFoundError:
            print(c.RED + 'no file to read - something went wrong' + c.END)
            raise

        bulk = []
        for lines in collection:
            bulk.append(lines)
        os.chmod(fpath, stat.S_IREAD)
        collection.close()

        bulk = ''.join(bulk)
        # cleans string - subs out excess newline characters
        # so that entries print cleanly. replaces w/ first letter occurance
        bulk = re.sub(c.SCAN_REGEX, r'\g<1>''', bulk)
        bulk = bulk.split(c.END_MARKER)
        del bulk[-1]  # remove newline element

        return bulk

    def refresh_collection(self):
        'after deletion of entry, re-write collection to reflect changes'

        try :
            # make collection writeable
            os.chmod(c.collection_TITLE, stat.S_IRWXU)
            refresh = open(c.collection_TITLE, 'w')
        except FileNotFoundError:
            print(c.RED + 'no file to modify - something went wrong' + c.END)
            raise

        for entry in self.collection:
            refresh.write(entry)
            refresh.write(c.END_MARKER + '\n\n')

        os.chmod(c.collection_TITLE, stat.S_IREAD)
        refresh.close()

    def wipe_collection(self):
        'completely delete collection'

        selection = input('\ndelete default collection? y/n\n')

        if selection == 'y':
            try:
                print(c.YELLOW + '\ndeleting...' + c.END)
                os.remove(c.collection_TITLE)
                print(c.PURPLE + os.path.abspath(c.collection_TITLE) + c.YELLOW + ' deleted' + c.END)
            except FileNotFoundError:
                # user machine removed file themselves after running program
                print(c.RED + '\nerror: file doesn\'t exist' + c.END)
                raise
        else:
            print('\nfile preserved')
            return

    def file_verify(self, f=c.collection_TITLE) :
        'checks for presence of entry file'

        return os.path.exists(f)

    def backup_collection(self):
        'creates a backup collection file'

        # uses 'copy' to preserve permissions
        # in case future update relies on permission at close
        try:
            copy(c.collection_TITLE, c.BACKUP_TITLE)
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
            copy(c.collection_TITLE, c.BACKUP_TITLE)
            print(c.YELLOW + '\nbackup updated as ' + c.PURPLE + os.path.abspath(c.BACKUP_TITLE) + c.END)
        except FileNotFoundError:
            # user machine removed file themselves after running program
            print(c.RED + '\nerror: bad backup' + c.END)
            raise

    def load_from_backup(self):
        'makes backup the running document'

        if not os.path.exists(c.BACKUP_TITLE):
            print('\nno backup found')
            return

        selection = input('\nrestore from backup? y/n\n')
        if selection == 'y':
            # make sure correct collection is retained
            try:
                os.remove(c.collection_TITLE)
            except FileNotFoundError:
                print(c.PURPLE + "creating new file, retaining backup..." + c.END)

            print(c.YELLOW + '\nrestoring...' + c.END)
            # backup -> running file
            try:
                os.rename(c.BACKUP_TITLE, c.collection_TITLE)
                # retain a copy
                copy(c.collection_TITLE, c.BACKUP_TITLE)
                print(c.YELLOW + 'restored from ' + c.PURPLE + os.path.abspath(c.BACKUP_TITLE) + c.END)
            except FileNotFoundError:
                # user machine removed file themselves after running program
                print(c.RED + '\nerror: bad backup' + c.END)
                raise

        else:
            print('\nload from backup cancelled')
            return

    def gen_config(self, active='idl', deff=c.DEFAULTS):
        'generate config file in pwd'

        folder = Path(c.DIR_NAME)
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'END_MARKER': deff[0],
                             'DATESTAMP_UNDERLINE': deff[1],
                             'collection_TITLE': active,
                             'BACKUP_TITLE': 'b_' + active,
                             'FIRST_MARKER': deff[2],
                             'SECOND_MARKER': deff[3],
                             'USE_TEXTBOX': deff[4]}

        try:
            configfile = open(folder / 'idl.ini', 'w')
        except FileNotFoundError:
            print(c.RED + 'no file to modify - something went wrong' + c.END)
            raise
        config.write(configfile)
        configfile.write(c.CONFIG_MESSAGE)
        configfile.close()

        print(c.YELLOW + '\nconfig updated as ' + c.PURPLE + os.path.abspath(folder / 'idl.ini') + c.END)

    def quick_delete(self):
        'quick-deletes the last entry made'

        # return if collection is empty
        self.collection = self.scan_collection()
        if (len(self.collection) == 0):
            print('\nnothing to delete')
            return

        answer = input('\ndelete last entry? y/n\n')
        if answer == 'y':
            print(c.YELLOW + '\ndeleting...' + c.END)
            del self.collection[-1]
            self.refresh_collection()
            print(c.YELLOW + 'deleted' + c.END)
            return
        else:
            print('\nnothing deleted')
            return
    
    def switch(self, new):
        'sets a new name for default collection'

        # if file doesn't exist, verify
        folder = Path(c.DIR_NAME)
        name = new + '.txt'
        path = folder / name
        if self.file_verify(path) == False:
            verify = input("\nno collection by that name. set as working collection? y/n\n")
            if verify != 'y':
                print("\nnothing modified")
                return

        # preserve modifications
        keep = [c.END_MARKER, c.DATESTAMP_UNDERLINE, c.FIRST_MARKER, c.SECOND_MARKER, c.USE_TEXTBOX]
        print("\nsetting " + c.PURPLE + new + ".txt" + c.END + "...")
        self.gen_config(new, keep)
        print("\n" + c.PURPLE + new + ".txt" + c.END + " is new working collection")

    def check_dir(self, dire=c.DIR_NAME):
        'checks for presence of a directory, and creates if not found'

        if not os.path.exists(dire):
            verify = input("\nno collection directory here. create? y/n\n")
            if verify != "y":
                print("\nno directory created")
                return False
            os.makedirs(dire)
            return True

    def wipe_all(self):
        'deletes entire contents folder'

        answer = input('\ndelete every collection in this directory? y/n\n')
        if answer != 'y':
            print('\nnothing deleted')
            return
        print(c.YELLOW + 'deleting all...' + c.END)
        try:
            rmtree(c.DIR_NAME)
        except Exception:
            print(c.RED + '\nsomething went wrong\n' + c.END)
            raise
        print(c.YELLOW + 'everything deleted' + c.END)