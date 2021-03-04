from os import path
from pathlib import Path
from peck.config_parser import ConParser

# ascii coloring
END = '\033[0m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RED = '\033[91m'

# name of the directory
DIR_NAME = Path.home() / 'pck'

VERSION = 'v2.4.1'

HELP = 'usage:\nfull: \'peck [arg]\'\nquick entry: \'peck [entry]\'\n\n\
alternatively, the title of entries with arg use can be one-lined like:\n\
\'peck [arg] [title]\'\n\
\ncommands:\n\
\'-l\': list out directory information\n\
\'-n\': new entry with both first and second sections\n\
\'-n1\': new entry with a first section\n\
\'-n2\': new entry with a second section\n\
\'-nt\': new title entry using a textbox\n\
\'-a\': new tagged entry. format: \'peck -a [tag] [title]\'\n\n\
\'-v\': view entries. follow with keyword to search\n\
\'-vf\': view a different collection in the same directory.\n       format: \
\'peck -vf: [collection name][opt keyword]\'\n\
\'-ds\': view entries on a specific date. format: \'peck -ds [mm/dd/yy]\'\n\
\'-t\': search for entries with a tag\n\
\'-del\': delete entry(s). format: \'peck -del [keyword]\'\n\
\'-q\': quick delete the last entry made\n\
\'-wipe\': delete default collection\n\
\'-wipe-all\': delete folder referencing this location\n\
\'-b\': create backup\n\
\'-load\': load entries from backup\n\
\'-config\': generate config file in reference folder.\n\
           if config exists, defaults reset.\n\
           updating config may outdate collection\n\
\'-s\': specify default collection file.\n\
      does not modify existing files. modifes / creates config file.'

SEPERATOR = ''

SCAN_REGEX = r'\n\n([A-Z])(?=[a-z]{2}\s[0-9]{2}[:][0-9]{2}[A-Z]{2}\s[A-Z][a-z]{2}\s[0-9]{2}\s[0-9]{4})'
VIEW_REGEX = r'[A-Z][a-z]{2}\s[0-9]{2}[:][0-9]{2}[A-Z]{2}\s[A-Z][a-z]{2}\s[0-9]{2}\s[0-9]{4}'
DATETIME = '%a %I:%M%p %b %d %Y'

CONFIG_MESSAGE = '\n# WARNING: updating may outdate collection in pwd\n\n\
# \'end_marker\' determines entry marker recorded in collection file. \
updating will outdate collection file in pwd.\n\
# \'datestamp_underline\' determines the series of underscores under the entry\
 date time stamp. may be changed without outdating anything.\n\
# \'collection_title\' defines the name of the default collection file. \
# set this to \
the desired default collection file, or change to create a new one.\n\
# \'backup_title\' defines the name of the current backup file. set this to \
the desired default backup file, or change to create a new one.\n\
# \'first_marker\' determines what should mark an entry\'s \'first\' \
section. may be changed without outdating anything.\n\
# \'second_marker\' determines what should mark an entry\'s \'second\' \
section. may be changed without outdating anything.\n\
# \'use_textbox\' can be set to false if textbox use is undesired.'

DEFAULTS = ['#*#*#*#*#*#*#*#*#*#*#*#', '-----------------------',
            '1st:', '2nd:', True]

# representation of the folder to use for the program instance
# works only with posix file path convention - notice the split at '/'
FOLDER = Path.home() / 'pck' / '_'.join(str(Path.cwd()).split('/')[-3:])

END_MARKER = DEFAULTS[0]
DATESTAMP_UNDERLINE = DEFAULTS[1]
COLLECTION_TITLE = FOLDER / 'pck.txt'
BACKUP_TITLE = FOLDER / 'b_pck.txt'
FIRST_MARKER = DEFAULTS[2]
SECOND_MARKER = DEFAULTS[3]
USE_TEXTBOX = DEFAULTS[4]

# use config values if present, else use default
if path.exists(FOLDER / 'pck.ini'):
    config = ConParser()
    values = config.parse(FOLDER / 'pck.ini')

    END_MARKER = values["end_marker"]
    DATESTAMP_UNDERLINE = values["date_underline"]

    jtitle_nopath = values["jtitle"]
    btitle_nopath = values["btitle"]

    COLLECTION_TITLE = FOLDER / jtitle_nopath
    BACKUP_TITLE = FOLDER / btitle_nopath

    FIRST_MARKER = values["first"]
    SECOND_MARKER = values["second"]
    USE_TEXTBOX = values["textbox_use"]

# used to determine prompt for entries with sections
SECOND = '\n\'enter\' key to open text box. ' + SECOND_MARKER + ' '
FIRST = '\n\'enter\' key to open text box. ' + FIRST_MARKER + ' '

# to be used in absence of text box
SECOND_NT = '\n' + SECOND_MARKER + '\n'
FIRST_NT = '\n' + FIRST_MARKER + '\n'
