import configparser
import os
from pathlib import Path

# ascii coloring
END = '\033[0m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RED = '\033[91m'

# name of the directory
DIR_NAME = "jnl"

HEADER = '\n---\n\
\033[35m\
jnl\033[0m\
\n---\n\
\033[36m\
v1.4.0\
\033[0m\
\033[33m\
\nmade by joseph barsness\
\033[0m\n\
\nthis is a command line tool for recording\
 and accessing things.\n'

HELP = '\nusage:\nfull: \'jnl [arg]\'\nquick entry: \'jnl [entry]\'\n\
alternatively, the title of entries with arg use can be one-lined like \'jnl [arg] [title]\'\n\
\narguements:\n\
\'-n\': new entry with both first and second sections\n\
\'-n1\': new entry with a first section\n\
\'-n2\': new entry with a second section\n\
\'-nt\': new title entry using a textbox\n\
\'-a\': new tagged entry. format: \'jnl -a [tag] [title]\'\n\n\
\'-v\': view entries. follow with keyword to search\n\
\'-t\': search for entries with a tag\n\
\'-del\': delete entry(s). format: \'jnl -del [keyword]\'\n\
\'-q\': quick delete the last entry made\n\
\'-wipe\': delete collection\n\
\'-b\': create backup\n\
\'-load\': load entries from backup\n\
\'-config\': generate config file in pwd. if config exists, defaults reset.\n\
           updating config may outdate collection\n\
\'-s\': specify default collection file.\n\
      does not modify existing files. modifes / creates config file.\n\
\nfirst / second sections are intended to make journals flexible in use.\n\
e.g. running -config and changing markers to \'where\' and \'when\''

# escape sequences for color
SEPERATOR = '<\>'

SCAN_REGEX = r'\n\n([A-Z])(?=[a-z]{2}\s[0-9]{2}[:][0-9]{2}[A-Z]{2}\s[A-Z][a-z]{2}\s[0-9]{2}\s[0-9]{4})'

CONFIG_MESSAGE = '\n# WRNG: updating may outdate journal in pwd\n\n\
# \'end_marker\' determines entry marker recorded in journal file. \
updating will outdate journal file in pwd.\n\
# \'datestamp_underline\' determines the series of underscores under the entry\
 date time stamp. may be changed without outdating anything.\n\
# \'journal_title\' determines the name of the journal file. set this to \
the desired default journal file, or change to create a new one.\n\
# \'backup_title\' determines the name of the backup file. set this to \
the desired default backup file, or change to create a new one.\n\
# \'first_marker\' determines what should preceed an entry\'s \'first\' \
section. may be changed without outdating anything.\n\
# \'second_marker\' determines what should preceed an entry\'s \'second\' \
section. may be changed without outdating anything.\n\
# \'use_textbox\' can be set to false if tk textbox use is undesired.'

DEFAULTS = ['#*#*#*#*#*#*#*#*#*#*#*#', '-----------------------',
            '1st:', '2nd:', True]

FOLDER = Path(DIR_NAME)

END_MARKER = DEFAULTS[0]
DATESTAMP_UNDERLINE = DEFAULTS[1]
JOURNAL_TITLE = FOLDER / 'jnl.txt'
BACKUP_TITLE = FOLDER / 'b_jnl.txt'
FIRST_MARKER = DEFAULTS[2]
SECOND_MARKER = DEFAULTS[3]
USE_TEXTBOX = DEFAULTS[4]

# use config values if present, else use default
if os.path.exists(FOLDER / 'jnl.ini'):
    try:
        # use pathlib to hide filepaths from user
        config = configparser.ConfigParser()
        config.read(FOLDER / 'jnl.ini')

        END_MARKER = config['DEFAULT']['END_MARKER']
        DATESTAMP_UNDERLINE = config['DEFAULT']['DATESTAMP_UNDERLINE']

        jtitle_nopath = config['DEFAULT']['JOURNAL_TITLE'] + '.txt'
        btitle_nopath = config['DEFAULT']['BACKUP_TITLE'] + '.txt'

        JOURNAL_TITLE = FOLDER / jtitle_nopath
        BACKUP_TITLE = FOLDER / btitle_nopath

        FIRST_MARKER = config['DEFAULT']['FIRST_MARKER']
        SECOND_MARKER = config['DEFAULT']['SECOND_MARKER']
        USE_TEXTBOX = config.getboolean('DEFAULT', 'USE_TEXTBOX')

    # indicates something is unable to be fixed
    except (configparser.ParsingError, ValueError, KeyError):
        print(RED + "\nsomething wrong with config file format. delete file or fix to proceed\n" + END)
        raise

# used to determine prompt for entries with sections
SECOND = '\n\'enter\' key to open text box. ' + SECOND_MARKER + ' '
FIRST = '\n\'enter\' key to open text box. ' + FIRST_MARKER + ' '

# to be used in absence of text box
SECOND_NT = '\n' + SECOND_MARKER + '\n'
FIRST_NT = '\n' + FIRST_MARKER + '\n'
