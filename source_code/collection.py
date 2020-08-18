import constants as c
import re
import os
import stat
from file_handle import FileHandle


class Collection:
    'a collection of entries'
    
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
            
            FileHandle.refresh_collection(self.collection)
            print(c.YELLOW + 'entries deleted' + c.END)

        else:
            print('\nentries preserved')
            return

    def scan_collection(self, fpath=c.COLLECTION_TITLE):
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
            FileHandle.refresh_collection(self.collection)
            print(c.YELLOW + 'deleted' + c.END)
            return
        else:
            print('\nnothing deleted')
            return
