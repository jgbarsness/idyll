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

    def scan_journal(self):
        'refreshes collection of journal entries'
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

    def random_entry(self):
        'prints random journal entry'
        # verify entry present
        if len(self.collection) > 0:
            print('\nrandom entry\n')
            random_entry = random.choice(self.collection)
            print(random_entry)
        else:
            print('\nnone found. check location of journal\n')

    def display_journal(self):
        'prints out entire journal'
        if len(self.collection) > 0:
            # print out entire journal
            print('\nentries\n')
            for entry in self.collection:
                print(entry)
        else:
            print('\nnone found. check location of journal\n')

    def show_keyword(self, key):
        'shows entries if keyword matches'
        # search for instances of keyword
        entry = [elmnt for elmnt in self.collection if key in elmnt]

        # if none were found, return
        if len(entry) == 0:
            print('\nno entry with that term. returning\n')
            return

        # if function can continue, print out entry
        print('\nentries containing',
              '\'' + key + '\'\n')
        for thing in entry:
            print(thing)

    def select(self):
        'call user selected function'
        selection = input('\nview full journal (j), del entry (del), ' +
                          'view random (o) or use keyword (k)?\n')

        if selection == 'o' or selection == 'random':
            self.random_entry()
        elif selection == 'k' or selection == 'key' or selection == 'keyword':
            user_key = input('\nenter a word to search for:\n')
            self.show_keyword(user_key)
        elif selection == 'j' or selection == 'journal':
            self.display_journal()
        elif selection == 'del' or selection == 'delete':
            criteria = input('\nenter a phrase to search for:\n')
            self.delete_entry(criteria)
        else:
            print('\nno selection - returning. run again if desired\n')
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

    def wipe_journal(self):
        'completely delete journal'
        selection = input('\nthis will delete your entire journal.' +
                          '\nare you sure? enter \'i am sure\' to proceed\n')

        if selection == 'i am sure':
            try:
                print('\ndeleting journal...')
                os.remove(c.JOURNAL_TITLE)
                print('journal deleted\n')
            except FileNotFoundError:
                print('no journal present\n')
        else:
            print('\nfile preserved. returning\n')
            return

    def delete_entry(self, entry):
        'bulk or single delete entries'
        # list of all occurances of key
        delete = [elmnt for elmnt in self.collection if entry in elmnt]

        # if none were found, return
        if len(delete) == 0:
            print('\nno entry with that term. returning\n')
            return

        # if function can continue, print out entry
        print('\nentries containing',
              '\'' + entry + '\'\n')
        for thing in delete:
            print(thing)

        choice = input('delete these entries? cannot be undone. '
                       'if unwanted entries are listed, further '
                       'specify search criteria.\nenter '
                       '\'i am sure\' to proceed\n')

        if choice == 'i am sure':
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

    def backup_journal(self):
        'creates a backup journal file'
        # uses 'copy' to preserve permissions
        # in case future update relies on permission at close
        self.file_check()
        print('\ncreating backup...')
        try:
            copy(c.JOURNAL_TITLE, c.BACKUP_TITLE)
            print('backup created as \'' + c.BACKUP_TITLE + '\'\n')
        except PermissionError:
            os.remove(c.BACKUP_TITLE)
            copy(c.JOURNAL_TITLE, c.BACKUP_TITLE)
            print('backup updated\n')

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
                          'be lost.\nenter \'i am sure\' to proceed\n')
        if selection == 'i am sure':
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
                             'NOTES_MARKER': '-n:',
                             'WHY_MARKER': '-w:'}

        configfile = open('journal_mngr.ini', 'w')
        config.write(configfile)
        configfile.write(c.CONFIG_MESSAGE)
        configfile.close()

        print('\nconfig updated in pwd as \'journal_mngr.ini\'\n')
