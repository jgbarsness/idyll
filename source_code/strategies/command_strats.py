from strategies.strat import CommandStrategy
from constants_routers.file_handle import FileHandle
import constants_routers.constants as c

'strategies used to modify and/or display collections'

class ViewStrat(CommandStrategy):
    'view / print strat'

    def call_command(self, collections: list, title: str):
        if not FileHandle.file_verify():
            print("\ndefault entry file doesn't exist")
            return []

        # if there is a keyword to search with
        if (len(title) != 0):
            criteria = title
            print('entries containing ' + '\'' + c.CYAN + criteria + c.END + '\':')
            if len(StratHelpers.show_keyword(title, collections)) != 0:
                print("\n" + str(len(StratHelpers.return_thing(title, collections))) + " entry(s)")

        # if no keyword is present, print out entire collection
        else:
            # check for formatted entries
            if (len(collections) != 0):
                print('all entries:')
                StratHelpers.print_entries(collections)
                print("\n" + str(len(collections)) + " entry(s)")
            else:
                # means that a file is present, but nothing could be parsed from it
                print('\nempty collection and/or invalid entry format')
        return collections

class TSearchStrat(CommandStrategy):
    'strat to search entries for tag'

    def call_command(self, collections: list, title: str):
        if not FileHandle.file_verify():
            print("\nno entry file")
            return []
        if (len(collections) != 0) and (len(title) != 0):
            print('searching for tag ' + '\'' + c.CYAN + title + c.END + '\':')
            if len(StratHelpers.show_keyword('(' + title + ')', collections)) != 0:
                print("\n" + str(len(StratHelpers.return_thing('(' + title + ')', collections))) + " entry(s)")
        else:
            print('\nnothing to show\nformat: idl -t [tag]')
        return collections

class DeleteModStrat(CommandStrategy):
    'returns a list of collections deleted by keyword. nothing modified'

    def call_command(self, collections: list, title: str):
        'bulk or single delete entries'

        mod_collections = collections.copy()
        delete = [elmnt for elmnt in collections if title in elmnt]
        # if nothing is returned by previous call, end
        if (len(delete) == 0):
            print('\nnothing to delete containing ' 
                  + '\'' + c.CYAN + title + c.END + '\'')
            return collections

        # if function can continue, print out entry
        print('to be deleted, containing ' + '\'' + c.CYAN + title + c.END + '\':')
        for thing in delete:
            print('\n' + thing + c.SEPERATOR)

        choice = input('\ndelete ' + str(len(delete)) + ' entries? y/n\n')

        if choice == 'y':
            print(c.YELLOW + '\ndeleting entries...' + c.END)

            # find all occurances
            for things in delete:
                # remove them
                mod_collections.remove(things)
            
            print(c.YELLOW + 'entries deleted' + c.END)
            return mod_collections

        else:
            print('\nentries preserved')
            return collections

class QuickDeleteStrat(CommandStrategy):
    'returns a representation of a quick-delete for the last entry made. nothing modified'

    def call_command(self, collections: list, title: str):
        # return if collection is empty
        if (len(collections) == 0):
            print('\nnothing to delete')
            return collections

        answer = input('\ndelete last entry? y/n\n')
        if answer == 'y':
            print(c.YELLOW + '\ndeleting...' + c.END)
            mod_collections = collections.copy()
            del mod_collections[-1]
            print(c.YELLOW + 'deleted' + c.END)
            return mod_collections
        else:
            print('\nnothing deleted')
            return collections

class StratHelpers():
    'helper methods'

    @staticmethod
    def show_keyword(key: str, container: list):
        'shows entries if keyword matches'

        entry = StratHelpers.return_thing(key, container)
        if (len(entry) == 0):
            print('\nnothing to show')
            return entry

        # if function can continue, print out entry
        StratHelpers.print_entries(entry)
        return entry

    @staticmethod
    def return_thing(key: str, container: list):
        'returns a list of all entries containing a keywork'

        # search for instances of keyword
        entry = [elmnt for elmnt in container if key in elmnt]

        return entry

    @staticmethod
    def print_entries(container):
        'used to print out things entries after search is ran'

        for thing in container:
            print('\n' + thing + c.SEPERATOR)
