from peck.a_strategy import CommandStrategy
from peck.file_handle import FileHandle
import peck.info_and_paths as c
from peck.modify_strats import StratHelpers
from datetime import datetime as dt
from re import match

'strategies used to display collections'


class ViewStrat(CommandStrategy):
    'view / print strat'

    def call_command(self, collections: list, title: str, path: str):
        if not ViewHelpers.vs_file_check():
            return

        # if there is a keyword to search with
        if (len(title) != 0):
            criteria = title
            print('entries containing ' + '\'' + c.BLUE + criteria
                  + c.END + '\':')
            if len(StratHelpers.show_keyword(title, collections)) != 0:
                ViewHelpers.print_num_entries(len(StratHelpers.return_thing(
                                              title,
                                              collections)),
                                              path)

        # if no keyword is present, print out entire collection
        else:
            # check for formatted entries
            if (len(collections) != 0):
                print('all entries:')
                StratHelpers.print_entries(collections)
                ViewHelpers.print_num_entries(len(collections),
                                              path)
            else:
                # means that a file is present, but nothing parsed from it
                print('\nempty collection and/or invalid entry format')


class TSearchStrat(CommandStrategy):
    'strat to search entries for tag'

    def call_command(self, collections: list, title: str, path: str):
        if not ViewHelpers.vs_file_check():
            return
        if (len(collections) != 0) and (len(title) != 0):
            print('searching for tag ' + '\'' + c.BLUE + title + c.END + '\':')
            if len(StratHelpers.show_keyword('(' + title + ')',
                   collections)) != 0:
                ViewHelpers.print_num_entries(len(StratHelpers.return_thing(
                                              '(' + title + ')',
                                              collections)),
                                              path)
        else:
            print('\nnothing to show\nformat: peck -t [tag]')


class DateSearch(CommandStrategy):
    'searches entries by date'

    def call_command(self, collections: list, title: str, path: str):
        if not ViewHelpers.vs_file_check():
            return
        if (len(collections) != 0) and (len(title) != 0):
            matches = self.search_by_date(collections, title)
            if len(matches) != 0:
                print('entries on ' + c.BLUE + str(title) + c.END + ':')
                StratHelpers.print_entries(matches)
                ViewHelpers.print_num_entries(len(matches),
                                              path)
            else:
                print('\nno matches on this date or bad date format')
        else:
            print('\nnothing to show\nformat: peck -ds [mm/dd/yy]')

    def search_by_date(self, collections: list, title: str) -> list:
        matches = []
        try:
            # the criteria date given from title
            criteria = dt.strptime(title, "%m/%d/%y")
        except ValueError:
            return []
        for note in collections:
            note_date = match(c.VIEW_REGEX, note).group(0)
            try:
                # replace call is used to standardize format
                note_date_obj = dt.strptime(note_date,
                                            c.DATETIME).replace(hour=00,
                                                                minute=00)
                # if the date is the same
                if note_date_obj == criteria:
                    matches.append(note)
            except ValueError:
                print('\n' + c.RED +
                      'error: entry parsing error. entry date format modified' +
                      c.END + '\n')
                return
        return matches


class ViewHelpers():
    'utility for view strats'

    @staticmethod
    def vs_file_check() -> bool:
        'checks file presence, prints any messages'

        if not FileHandle.file_verify():
            print("\ndefault entry file doesn't exist")
            return False
        else:
            return True

    @staticmethod
    def print_num_entries(num: int, place: str) -> None:
        'prints out the count of entries to be printed'

        print(str(num) + " entry(s) in " + str(place))
