from mod_behaviors.a_strategy import CommandStrategy
from constants.file_handle import FileHandle
import constants.info_and_paths as c

'strategies used to modify collections'


class DeleteModStrat(CommandStrategy):
    'returns a list of collections deleted by keyword. nothing modified'

    def call_command(self, collections: list, title: str, path: str) -> bool:
        'bulk or single delete entries'

        delete = StratHelpers.return_thing(title, collections)
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

    def call_command(self, collections: list, title: str, path: str) -> bool:
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
