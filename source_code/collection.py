import random
import re
import os
import stat


class Collection:
    'a collection of entries. manages file storage'
    def __init__(self):
        self.collection = []

    def scan_journal(self):
        'refreshes collection of journal entries'
        journal = open('journal.txt', 'r')

        bulk = []
        for lines in journal:
            bulk.append(lines)
        journal.close()

        bulk = ''.join(bulk)
        # cleans string - subs out excess newline characters
        bulk = re.sub('\n\n([A-Z])(?=[a-z]{2}\s[A-Z][a-z]{2}'
                      '\s[0-9]{2}\s[0-9]{2}[:][0-9]{2}[:][0-9]'
                      '{2}\s[0-9]{4})', '\g<1>''', bulk)
        bulk = bulk.split('------------\nend_of_entry\n------------')
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
            print('\nnone found. check location of journal.txt\n')

    def display_journal(self):
        'prints out entire journal'
        if len(self.collection) > 0:
            # print out entire journal
            print('\nentries\n')
            for entry in self.collection:
                print(entry)
        else:
            print('\nnone found. check location of journal.txt\n')

    def show_keyword(self, key):
        'shows entry if keyword matches'
        # search for instances of keyword
        entry = [elmnt for elmnt in self.collection if key in elmnt]

        # if none were found, return
        if len(entry) == 0:
            print('\nno entry with that term. returning\n')
            return

        # if function can continue, print out entry
        # pad '-' characters as appropriate
        padding = ''.join(['-' for _ in range(len(str(key)) + 3)])
        print('\nrandom entry containing',
              '\'' + key + '\'\n')
        print(random.choice(entry))

    def select(self):
        'call user selected function'
        selection = input('\nview full journal (j), ' +
                          'view random (o) or use keyword (k)?\n')

        if selection == 'o' or selection == 'random':
            self.random_entry()
        elif selection == 'k' or selection == 'key' or selection == 'keyword':
            user_key = input('\nenter a word to search for:\n')
            self.show_keyword(user_key)
        elif selection == 'j' or selection == 'journal':
            self.display_journal()
        else:
            print('\nno selection - returning. run again if desired\n')
            return

    def file_check(self):
        '''check if file is present. if so, close. if not, create.
        make file writable if file exists'''
        try:
            os.chmod('journal.txt', stat.S_IRWXU)
        except FileNotFoundError:
            pass

        file_check = open('journal.txt', 'a+')
        file_check.close()

        # make file read only
        os.chmod('journal.txt', stat.S_IREAD)

    def wipe_journal(self):
        'completely delete journal'
        selection = input('\nthis will delete your entire journal.' +
                          '\nare you sure? enter \'i am sure\' to proceed\n')

        if selection == 'i am sure':
            try:
                print('\ndeleting journal...')
                os.remove('journal.txt')
                print('journal deleted\n')
            except FileNotFoundError:
                print('no file present. try running a command\n')
        else:
            print('\nfile preserved. returning\n')
            return
