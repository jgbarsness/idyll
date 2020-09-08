from mod_behaviors.i_behavior import CommandStrategy
from constants.file_handle import FileHandle
import constants.constants as c

'strategies used to modify and/or display collections'

class ViewStrat(CommandStrategy):
    'view / print strat'

    def call_command(self, collections: list, title: str):
        if not FileHandle.file_verify():
            print("\ndefault entry file doesn't exist")
            return

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
        return

class TSearchStrat(CommandStrategy):
    'strat to search entries for tag'

    def call_command(self, collections: list, title: str):
        if not FileHandle.file_verify():
            print("\nno entry file")
            return
        if (len(collections) != 0) and (len(title) != 0):
            print('searching for tag ' + '\'' + c.CYAN + title + c.END + '\':')
            if len(StratHelpers.show_keyword('(' + title + ')', collections)) != 0:
                print("\n" + str(len(StratHelpers.return_thing('(' + title + ')', collections))) + " entry(s)")
        else:
            print('\nnothing to show\nformat: idl -t [tag]')
        return

class DeleteModStrat(CommandStrategy):
    'returns a list of collections deleted by keyword. nothing modified'

    def call_command(self, collections: list, title: str) -> bool:
        'bulk or single delete entries'

        delete = [elmnt for elmnt in collections if title in elmnt]
        # if nothing is returned by previous call, end
        if (len(delete) == 0):
            print('\nnothing to delete containing ' 
                  + '\'' + c.CYAN + title + c.END + '\'')
            return False

        # if function can continue, print out entry
        print('to be deleted, containing ' + '\'' + c.CYAN + title + c.END + '\':')
        for thing in delete:
            print('\n' + thing + c.SEPERATOR)

        choice = input('\ndelete ' + str(len(delete)) + ' entries? y/n\n')

        if choice == 'y':
            # find all occurances
            for things in delete:
                # remove them
                collections.remove(things)
            
            return True

        else:
            print('\nentries preserved')
            return False

class QuickDeleteStrat(CommandStrategy):
    'returns a representation of a quick-delete for the last entry made. nothing modified'

    def call_command(self, collections: list, title: str) -> bool:
        # return if collection is empty
        if (len(collections) == 0):
            print('\nnothing to delete')
            return False

        answer = input('\ndelete last entry? y/n\n')
        if answer == 'y':
            del collections[-1]
            return True
        else:
            print('\nnothing deleted')
            return False

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
