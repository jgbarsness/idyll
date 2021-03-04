from configparser import ConfigParser, ParsingError
from os import path
from pathlib import Path
import peck.info_and_paths as c


class ConParser:

    @staticmethod
    def parse(path) -> dict:
        'handles config file parsing'

        try:
            config = ConfigParser()
            config.read(path)
            values = {
                "end_marker": config['DEFAULT']['END_MARKER'],
                "date_underline": config['DEFAULT']['DATESTAMP_UNDERLINE'],
                "jtitle": config['DEFAULT']['COLLECTION_TITLE'] + '.txt',
                "btitle": config['DEFAULT']['BACKUP_TITLE'] + '.txt',
                "first":  config['DEFAULT']['FIRST_MARKER'],
                "second": config['DEFAULT']['SECOND_MARKER'],
                "textbox_use": config.getboolean('DEFAULT', 'USE_TEXTBOX')
            }
            return values
        # indicates parsing error
        except (ParsingError, ValueError, KeyError):
            print(c.RED + "\nerror: something wrong with config file format. delete ",
                  "file or fix to proceed\n" + c.END)
            return
