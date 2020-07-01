import constants as c
import random
import re
import os
import stat
from shutil import copy
import configparser


class Collection:
    'a collection of entries. manages file storage'
    def __init__(self):
        self.collection = []

    def check_for_entries(self, to_check):
        'checks if any entries are present'

        if len(to_check) == 0:
            return False
        else:
            return True

    def check_for_thing(self, key):
        'returns a list of all entries containing a keywork'

        # search for instances of keyword
        entry = [elmnt for elmnt in self.collection if key in elmnt]

        # if none were found, return
        if len(entry) == 0:
            print('\nno entry with that term. returning\n')
            return entry

        return entry

    def show_keyword(self, key):
        'shows entries if keyword matches'

        entry = self.check_for_thing(key)
        if self.check_for_entries(entry) is False:
            return

        # if function can continue, print out entry
        self.print_entries(key, entry)

    def display_journal(self):
        'prints out entire journal'

        if self.check_for_entries(self.collection):
            # print out entire journal
            print('\nentries\n')
            for entry in self.collection:
                print(entry)
        else:
            print('\nnone found. check location of journal\n')

    def print_entries(self, criteria, container):
        'used to print out things entries after search is ran'

        print('\nentries containing',
              '\'' + criteria + '\'\n')
        for thing in container:
            print(thing)

    def delete_entry(self, entry):
        'bulk or single delete entries'

        delete = self.check_for_thing(entry)
        # if nothing is returned by previous call, end
        if self.check_for_entries(delete) is False:
            return

        # if function can continue, print out entry
        self.print_entries(entry, delete)

        choice = input('delete these entries? cannot be undone. '
                       'if unwanted entries are listed, further '
                       'specify search criteria.\nenter '
                       '\'p\' to proceed\n')

        if choice == 'p':
            print('\ndeleting entries...')

            # find all occurances
            for things in delete:
                # remove them
                self.collection.remove(things)

            print('entries deleted\n')
            # refresh entries
            self.file_check()
            self.refresh_journal()

        else:
            print('\nentries preserved. returning\n')
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

        selection = input('\nthis will delete your entire journal.' +
                          '\nare you sure? enter \'p\' to proceed\n')

        if selection == 'p':
            try:
                print('\ndeleting journal...')
                os.remove(c.JOURNAL_TITLE)
                print('journal deleted\n')
            except FileNotFoundError:
                print('no journal present\n')
        else:
            print('\nfile preserved. returning\n')
            return

    def file_check(self):
        '''check if file is present. if so, close. if not, create.
        make file writable if file exists'''

        try:
            os.chmod(c.JOURNAL_TITLE, stat.S_IRWXU)
        except FileNotFoundError:
            pass

        file_check = open(c.JOURNAL_TITLE, 'a+')
        file_check.close()

        # make file read only
        os.chmod(c.JOURNAL_TITLE, stat.S_IREAD)

    def backup_journal(self):
        'creates a backup journal file'

        # uses 'copy' to preserve permissions
        # in case future update relies on permission at close
        self.file_check()
        try:
            copy(c.JOURNAL_TITLE, c.BACKUP_TITLE)
            print('\nbackup created as \'' + c.BACKUP_TITLE + '\'\n')
        except PermissionError:
            # verify desired behavior
            choice = input('\nbackup copy detected. are you sure you'
                           ' want to override? enter \'p\' if so.\n')
            if choice == 'p':
                pass
            else:
                print('\nno update made. returning\n')
                return

            os.remove(c.BACKUP_TITLE)
            # retain a backup copy
            copy(c.JOURNAL_TITLE, c.BACKUP_TITLE)
            print('\nbackup updated as \'' + c.BACKUP_TITLE + '\'\n')

    def load_from_backup(self):
        'makes backup the running document'

        try:
            open(c.BACKUP_TITLE, 'r')
            pass
        except FileNotFoundError:
            print('\nno backup found\n')
            return
        selection = input('\nrestore journal from backup?\nif backup'
                          ' is outdated, recent journal entries will '
                          'be lost.\nenter \'p\' to proceed\n')
        if selection == 'p':
            # make sure correct journal is retained
            try:
                os.remove(c.JOURNAL_TITLE)
            except FileNotFoundError:
                pass

            print('\nrestoring')
            # backup -> running file
            os.rename(c.BACKUP_TITLE, c.JOURNAL_TITLE)
            # retain a copy
            copy(c.JOURNAL_TITLE, c.BACKUP_TITLE)
            print('journal restored from \'' + c.BACKUP_TITLE + '\'\n')

        else:
            print('\nload from backup cancelled. returning\n')
            return

    def gen_config(self):
        'generate config file in pwd'

        config = configparser.ConfigParser()
        config['DEFAULT'] = {'END_MARKER': '#*#*#*#*#*#*#*#*#*#*#*#',
                             'DATESTAMP_UNDERLINE': '-----------------------',
                             'JOURNAL_TITLE': 'journal',
                             'BACKUP_TITLE': 'backup_journal',
                             'FIRST_MARKER': '1st:',
                             'SECOND_MARKER': '2nd:',
                             'USE_TEXTBOX': 'true'}

        configfile = open('jnl.ini', 'w')
        config.write(configfile)
        configfile.write(c.CONFIG_MESSAGE)
        configfile.close()

        print('\nconfig updated in pwd as \'jnl.ini\'\n')

    def quick_delete(self):
        'quick-deletes the last entry made'

        # return if journal is empty
        self.scan_journal()
        if not self.check_for_entries(self.collection):
            print('\nnothing to delete\n')
            return

        answer = input('\ndelete last entry? \'p\' to proceed\n')
        if answer == 'p':
            print('\ndeleting...')
            del self.collection[-1]
            self.refresh_journal()
            print('deleted.\n')
            return
        else:
            print('\nnothing deleted\n')
            return
