## jnl <br />
is a command line tool used to create and manage journal entries. entries are managed in 'jnl.txt'. generating a config file using '-config' allows for customization of file titles, attributes of entries, and preferences.<br /><br />
packaged on OSX<br />
```sudo ln -s [...dist/jnl/jnl] [/usr/local/bin]``` to run from root using 'jnl'
#### using:

jnl [sys_arg] [title_or_keyword]<br />
or<br />
jnl [entry]

#### arguments:

'**-n**': new entry with both first and second sections<br />
'**-n1**': new entry with first section<br />
'**-n2**': new entry with second section<br />
'**-nt**': new entry using a textbook. ignores config file preferences<br />
'**-a**': new tagged entry. syntax: jnl -a [tag] [entry]<br />
'**-v**': view journal. syntax: jnl -v // jnl -v [keyword]<br />
'**-t**': search for entries with a tag<br />
'**-wipe**': delete entire journal<br />
'**-b**': create backup of journal<br />
'**-load**': load entries from backup<br />
'**-config**': generate config file in pwd. if config exists, defaults reset.
updating config may outdate journal<br />
'**-del**': delete entry<br />
'**-q**': quick delete the last entry made

first / second sections are intended to make journals flexible in use.<br />
e.g. running -config and changing the markers to 'where' and 'when'