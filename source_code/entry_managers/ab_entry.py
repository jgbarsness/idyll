import os
import stat
import datetime as dt
import constants_routers.constants as c
from entry_managers.entrybox import TextBox
from entry_managers.entry_writer import EntryWriter
from abc import ABC, abstractmethod


class AEntry(ABC):
    'an abstract entry to be stored in the collection'
    
    def __init__(self, passed_title):
        'accepts a title and an optional shortcut'
        self.recorded_datetime = dt.datetime.now().strftime('%a %I:%M%p %b %d %Y')
        self.title = passed_title

    @abstractmethod
    def begin_entry(self) -> None:
        'initializes textboxes, records input, manages call to write'

        try:
            os.chmod(c.COLLECTION_TITLE, stat.S_IRWXU)
        except FileNotFoundError:
            # permission handling will be passed down if continued
            check = input("\nno collection file in pwd. create? y/n\n")
            if check != 'y':
                print("\ncollection not created")
                return

    @abstractmethod
    def format_readability(self):
        'sets fields to "N/A" if empty'

        if self.title is None or self.title == '':
            self.title = 'N/A'

    def printout(self):
        'helper method to display entry title post-write'

        print('\nnew entry in ' + c.PURPLE + os.path.abspath(c.COLLECTION_TITLE) + c.END +
              '\ntitled: ' + '\'' + self.title + '\'')

    @abstractmethod
    def write(self):
        'write to file'
        pass
