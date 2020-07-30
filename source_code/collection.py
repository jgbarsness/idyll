import constants as c
import random
import re
import os
import stat
from shutil import copy
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
            self.refresh_journal()
            print(c.YELLOW + 'entries deleted' + c.END)

        else:
            print('\nentries preserved')
            return

    def scan_journal(self):
        'refreshes collection list of journal entries'

        os.chmod(c.JOURNAL_TITLE, stat.S_IRWXU)
        journal = open(c.JOURNAL_TITLE, 'r')

        bulk = []
        for lines in journal:
            bulk.append(lines)
        os.chmod(c.JOURNAL_TITLE, stat.S_IREAD)
        journal.close()

        bulk = ''.join(bulk)
        # cleans string - subs out excess newline characters
        # so that entries print cleanly. replaces w/ first letter occurance
        bulk = re.sub(c.SCAN_REGEX, r'\g<1>''', bulk)
        bulk = bulk.split(c.END_MARKER)
        del bulk[-1]  # remove newline element

        self.collection = bulk

    def refresh_journal(self):
        'after deletion of entry, re-write journal to reflect changes'

        # make journal writeable
        os.chmod(c.JOURNAL_TITLE, stat.S_IRWXU)
        refresh = open(c.JOURNAL_TITLE, 'w')

        for entry in self.collection:
            refresh.write(entry)
            refresh.write(c.END_MARKER + '\n\n')

        os.chmod(c.JOURNAL_TITLE, stat.S_IREAD)
        refresh.close()

    def wipe_journal(self):
        'completely delete journal'

        selection = input('\ndelete all? y/n\n')

        if selection == 'y':
            try:
                print(c.YELLOW + '\ndeleting...' + c.END)
                os.remove(c.JOURNAL_TITLE)
                print(c.PURPLE + os.path.abspath(c.JOURNAL_TITLE) + c.YELLOW + ' deleted' + c.END)
            except FileNotFoundError:
                print('nothing present')
        else:
            print('\nfile preserved')
            return

    def file_verify(self, f=c.JOURNAL_TITLE) :
        'checks for presence of entry file'

        return os.path.exists(f)

    def backup_journal(self):
        'creates a backup journal file'

        # uses 'copy' to preserve permissions
        # in case future update relies on permission at close
        try:
            copy(c.JOURNAL_TITLE, c.BACKUP_TITLE)
            print(c.YELLOW + '\nbackup created as ' + c.PURPLE + os.path.abspath(c.BACKUP_TITLE)+ c.END)
        except PermissionError:
            # verify desired behavior
            choice = input('\nbackup detected. overwrite? y/n\n')
            if choice == 'y':
                pass
            else:
                print('\nno update made')
                return

            os.remove(c.BACKUP_TITLE)
            # retain a backup copy
            copy(c.JOURNAL_TITLE, c.BACKUP_TITLE)
            print(c.YELLOW + '\nbackup updated as ' + c.PURPLE + os.path.abspath(c.BACKUP_TITLE) + c.END)

    def load_from_backup(self):
        'makes backup the running document'

        try:
            open(c.BACKUP_TITLE, 'r')
            pass
        except FileNotFoundError:
            print('\nno backup found')
            return
        selection = input('\nrestore from backup? y/n\n')
        if selection == 'y':
            # make sure correct journal is retained
            try:
                os.remove(c.JOURNAL_TITLE)
            except FileNotFoundError:
                pass

            print(c.YELLOW + '\nrestoring...' + c.END)
            # backup -> running file
            os.rename(c.BACKUP_TITLE, c.JOURNAL_TITLE)
            # retain a copy
            copy(c.JOURNAL_TITLE, c.BACKUP_TITLE)
            print(c.YELLOW + 'restored from ' + c.PURPLE + os.path.abspath(c.BACKUP_TITLE) + c.END)

        else:
            print('\nload from backup cancelled')
            return

    def gen_config(self, active='jnl', deff=c.DEFAULTS):
        'generate config file in pwd'

        folder = Path(c.DIR_NAME)
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'END_MARKER': deff[0],
                             'DATESTAMP_UNDERLINE': deff[1],
                             'JOURNAL_TITLE': active,
                             'BACKUP_TITLE': 'b_' + active,
                             'FIRST_MARKER': deff[2],
                             'SECOND_MARKER': deff[3],
                             'USE_TEXTBOX': deff[4]}

        configfile = open(folder / 'jnl.ini', 'w')
        config.write(configfile)
        configfile.write(c.CONFIG_MESSAGE)
        configfile.close()

        print(c.YELLOW + '\nconfig updated as ' + c.PURPLE + os.path.abspath(folder / 'jnl.ini') + c.END)

    def quick_delete(self):
        'quick-deletes the last entry made'

        # return if journal is empty
        self.scan_journal()
        if (len(self.collection) == 0):
            print('\nnothing to delete')
            return

        answer = input('\ndelete last entry? y/n\n')
        if answer == 'y':
            print(c.YELLOW + '\ndeleting...' + c.END)
            del self.collection[-1]
            self.refresh_journal()
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
                print("\nnothing created")
                return False
            os.makedirs(dire)
            return True
