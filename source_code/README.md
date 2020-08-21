## idyll <br />
is a command line tool used to create and manage entries. entries are managed in '[cur_dir]/idl'. generating a config file using '-config' allows for customization of file titles, attributes of entries, and preferences.<br /><br />
packaged on macOS<br />
```sudo ln -s [...dist/idl/idl] [/usr/local/bin]``` to install from current folder location
#### using:

idl [sys_arg] [title_or_keyword]<br />
or<br />
idl [entry]

#### arguments:

'**-n**': new entry with both first and second sections<br />
'**-n1**': new entry with first section<br />
'**-n2**': new entry with second section<br />
'**-nt**': new entry using a textbox. ignores config file preferences<br />
'**-a**': new tagged entry. syntax: idl -a [tag] [entry]<br />
'**-v**': view entries. syntax: idl -v // idl -v [keyword]<br />
'**-t**': search for entries with a tag<br />
'**-wipe**': delete entire idl<br />
'**-wipe-all**': delete collection folder in pwd<br />
'**-b**': create backup of idl<br />
'**-load**': load entries from backup<br />
'**-config**': generate config file in pwd. if config exists, defaults reset.
updating config may outdate idl<br />
'**-s**': specify default collection file.
does not modify existing files. modifes / creates config file.<br />
'**-del**': delete entry<br />
'**-q**': quick delete the last entry made

first / second sections are intended to make collections flexible in use.<br />
e.g. running -config and changing the markers to 'where' and 'when'
