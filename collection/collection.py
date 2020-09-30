import constants.constants as c
from os import chmod, path
from stat import S_IRWXU, S_IREAD
from constants.file_handle import FileHandle
from pathlib import Path
from mod_behaviors.a_strategy import CommandStrategy
from re import sub


class Collection:
    'a collection of entries'
    
    def __init__(self, strategy: CommandStrategy, path_to_file):
        self.collection = self.scan_collection(path_to_file)
        # strategies used for display. file mod left to entry write class
        self._strategy = strategy

    @property
    def strategy(self) -> CommandStrategy:
        'reference to strategy'

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: CommandStrategy):
        'strategy setter'

        self._strategy = strategy

    def call_strat(self, title: str) -> bool:
        'calls strategy on collection'

        return self._strategy.call_command(self.collection, title)

    def scan_collection(self, fpath=c.COLLECTION_TITLE):
        'returns collection list of collection entries'

        if (fpath == None or not path.exists(fpath)):
            return []

        chmod(fpath, S_IRWXU)
        try:
            collection = open(fpath, 'r')
        except FileNotFoundError:
            print(c.RED + 'no file to read - something went wrong' + c.END)
            raise

        bulk = []
        for lines in collection:
            bulk.append(lines)
        chmod(fpath, S_IREAD)
        collection.close()

        bulk = ''.join(bulk)
        # cleans string - subs out excess newline characters
        # so that entries print cleanly. replaces w/ first letter occurance
        bulk = sub(c.SCAN_REGEX, r'\g<1>''', bulk)
        bulk = bulk.split(c.END_MARKER)
        del bulk[-1]  # remove newline element

        return bulk
