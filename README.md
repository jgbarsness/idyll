## journal mngr <br />
is a command line tool used to create and manage journal entries

#### documentation:
 'journal' runs main program. can be followed by a sys argument

#### optional sys arguements:
 '**-e**': new entry, title only <br /> '**-n**': new entry with both a notes and a why section <br /> '**-ng**': new entry with a notes section <br /> '**-nw**': new entry with a why section <br />
'**-v**': view journal <br />
'**-wipe**': delete entire journal <br />
'**-b**': create backup of journal

#### 'hidden' commands:

**'wipe'**: permanently delete all entries<br />
**'backup'**: create a backup copy of entire journal<br />
**'load'**: load entries from backup<br />
**'config'**: creates config .ini in pwd. 'journal_title' and 'backup_title' 	values can be changed to create multiple journals in the same pwd, with the 		current title reflecting the running journal and/or the preferred backup file. 	if a change to the entry marker is made, journal in pwd may become outdated. can 	delete .ini or re-run 'config' to restore defaults<br />