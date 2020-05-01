journal manager is a command line tool used to create and manage journal entries.

install instructions for running from shell:<br /> run `sudo ln -s /path_to_journal_unix_executable /usr/local/bin`<br /> sub the first path for your own personal location of the journal executable in the 'dist' folder<br /> entries are stored as 'journal.txt'

documentation:<br /> 'journal' runs main program. can be followed by a sys argument

optional sys arguements:<br /> '-e': new entry, title only<br /> '-n': new entry with both a notes and a why section<br /> '-ng': new entry with a notes section<br /> '-nw': new entry with a why section<br />
'-v': view journal<br />
'-wipe': delete entire journal<br />
'-b': create backup of journal

'hidden' commands:<br />
'wipe': permanently delete all entries<br />
'backup': create a backup copy of entire journal<br />
'load': load entries from backup<br />

alternatively, journal.py can be run, and journal entries will be maintained in the folder

know bugs/considerations:<br />
if one-lining with a sys arguement, you must escape non-alphanumerical characters (e.g. journal -e what\\'s up)<br />
uses a string marker to determine entry stop / starts. if you include this marker in an entry, that specific entry will behave abnormally. marker is unique enough to avoid all but intentional use.