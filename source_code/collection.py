import constants as c
import random
import re
import os
import stat
from shutil import copy
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
        print(c.YELLOW + 'to be deleted, containing ' + c.END + '\'' + c.CYAN + entry + c.END + '\':')
        self.print_entries(delete)

        choice = input('\ndelete? y/n\n')

        if choice == 'y':
            print(c.YELLOW + '\ndeleting entries...' + c.END)

            # find all occurances
            for things in delete:
                # remove them
                self.collection.remove(things)

            print(c.YELLOW + 'entries deleted' + c.END)
            # refresh entries
            self.file_check()
            self.refresh_journal()

        else:
            print('\nentries preserved')
            return

    def scan_journal(self):
        'refreshes collection list of journal entries'

        journal = open(c.JOURNAL_TITLE, 'r')

        bulk = []
        for lines in journal:
            bulk.append(lines)
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
                print(c.PURPLE + c.JOURNAL_TITLE + c.YELLOW + ' deleted' + c.END)
            except FileNotFoundError:
                print('nothing present')
        else:
            print('\nfile preserved')
            return

    def file_check(self):
        '''check if file is present. if so, close. if not, create.
        make file read-only'''

        try:
            os.chmod(c.JOURNAL_TITLE, stat.S_IRWXU)
        except FileNotFoundError:
            pass

        file_check = open(c.JOURNAL_TITLE, 'a+')
        file_check.close()

        # make file read only
        os.chmod(c.JOURNAL_TITLE, stat.S_IREAD)

    def file_verify(self) :
        'checks for presence of entry file'

        try:
            os.chmod(c.JOURNAL_TITLE, stat.S_IRWXU)
            return True
        except FileNotFoundError:
            return False

    def backup_journal(self):
        'creates a backup journal file'

        # uses 'copy' to preserve permissions
        # in case future update relies on permission at close
        try:
            copy(c.JOURNAL_TITLE, c.BACKUP_TITLE)
            print(c.YELLOW + '\nbackup created as ' + c.PURPLE + c.BACKUP_TITLE + c.END)
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
            print(c.YELLOW + '\nbackup updated as ' + c.PURPLE + c.BACKUP_TITLE + c.END)

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
            print(c.YELLOW + 'restored from ' + c.PURPLE + c.BACKUP_TITLE + c.END)

        else:
            print('\nload from backup cancelled')
            return

    def gen_config(self):
        'generate config file in pwd'

        config = configparser.ConfigParser()
        config['DEFAULT'] = {'END_MARKER': '#*#*#*#*#*#*#*#*#*#*#*#',
                             'DATESTAMP_UNDERLINE': '-----------------------',
                             'JOURNAL_TITLE': 'jnl',
                             'BACKUP_TITLE': 'b_jnl',
                             'FIRST_MARKER': '1st:',
                             'SECOND_MARKER': '2nd:',
                             'USE_TEXTBOX': 'true'}

        configfile = open('jnl.ini', 'w')
        config.write(configfile)
        configfile.write(c.CONFIG_MESSAGE)
        configfile.close()

        print(c.YELLOW + '\nconfig updated in pwd as ' + c.PURPLE + 'jnl.ini' + c.END)

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
