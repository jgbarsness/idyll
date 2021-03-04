from os import path, chmod
from stat import S_IRWXU
from datetime import datetime
import peck.info_and_paths as c
from abc import ABC, abstractmethod


class AEntry(ABC):
    'an abstract entry to be stored in the collection'
    
    def __init__(self, passed_title):
        self.recorded_datetime = str(datetime.now().strftime(c.DATETIME))
        self.title = passed_title
        self.print = True

    @abstractmethod
    def begin_entry(self) -> None:
        'initializes textboxes, records input, manages call to write'

        if (path.exists(c.COLLECTION_TITLE)):
            chmod(c.COLLECTION_TITLE, S_IRWXU)
        else:
            # permission handling will be passed down if continued
            check = input("\nno collection file in directory. create? y/n\n")
            if check != 'y':
                print("\ncollection file not created")
                # indicate that the object has not been fully instantiated
                self.print = False

    @abstractmethod
    def format_readability(self):
        'sets fields to "N/A" if empty'

        if self.title is None or self.title == '':
            self.title = 'N/A'

    def printout(self):
        'helper method to display entry details to console'

        print('\nnew entry in ' + c.PURPLE + path.abspath(c.COLLECTION_TITLE) + c.END +
              '\ntitled: ' + '\'' + self.title + '\'')

    @abstractmethod
    def write(self):
        'write to file'
        pass
