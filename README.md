journal manager is a command line tool used to create and manage journal entries.

install instructions for running from shell:<br /> run `sudo ln -s /Users/YOUR_NAME/Downloads/journal_manager-master/dist/journal/journal /usr/local/bin`<br /> if necessary, sub the first path for your own personal location of the journal executable in the 'dist' folder<br /> entries are stored as 'journal.txt'

documentation:<br /> 'journal' runs main program. can be followed by a sys argument

optional sys arguements:<br /> '-e': new entry, title only<br /> '-n': new entry with both a notes and a why section<br /> '-ng': new entry with a notes section<br /> '-nw': new entry with a why section<br />

alternatively, journal.py can be run, and journal entries will be maintained in the folder

know bugs:<br />
one-lining with '-e' has not been configured with entry points. characters like ''', '(', ';', etc. will be interpreted as console-specific commands and will misdirect input<br />
uses a string marker to determine entry stop / starts. if you include this marker in an entry, that specific entry will behave abnormally. marker is unique enough to avoid all but intentional use.