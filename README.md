## idyll <br />
is a command line tool used to create and manage text entries.<br /><br />
packaged on macOS<br />
to install from current folder location:<br />
```sudo ln -s [your path to bin/idl/idl] /usr/local/bin``` to install from current folder location
#### using:

```idl [command] [keyword (if appropriate)]```<br />
or for a quick entry:<br />
```idl [entry]```

things are organized within the 'idl' folder of whatever directory is currently the pwd. this folder will be created on first use within a directory. generating a config file using '-config' allows for customization of file titles, attributes of entries, and preferences. the switch (-s) command, described below, defines what collection file idyll will default to across instances. for example, if a pwd's idl.ini attribute 'collection_title' is set to 'idl.txt', running 'idl -v' will print out entries in this file. if i have another collection file in this directory, 'good_ideas.txt', running 'idl -s good_ideas', then 'idl -v', the entries in 'good_ideas.txt' will print out. 

to create a new collection file in the pwd, you can manually set the config file's 'collection_title' attribute to the new desired name, or you can run 'idl -s [new_name]' to create this file automatically on the next attempt to create an entry. running 'idl' will print a header with useful information on the current pwd's collection files.

config attributes allow various changes to how idyll file i/o functions. for example, if you want the date stamp to be underlined differently, this attribute can be modified. if you want a different string to mark the end of an entry, this can be modified. it should be noted that changing things integral to how the program functions, such as an entry end marker, current collection files may become outdated and function irregularity. more documentation can be found in the config file itself.

suggestions for use: to-do list, dream journal, version note manager, recipe experimentation database, anything that you want to keep track of paired with the time you remembered to record it
#### commands:

'**-n**': new entry with both first and second sections<br />
'**-n1**': new entry with first section<br />
'**-n2**': new entry with second section<br />
'**-nt**': new entry using a textbox. ignores config file preferences<br />
'**-a**': new tagged entry. syntax: idl -a [tag] [entry]<br />
'**-v**': view entries. syntax: idl -v // idl -v [keyword]<br />
'**-t**': search for entries with a tag<br />
'**-wipe**': delete entire idl<br />
'**-wipe-all**': delete collection folder in pwd<br />
'**-b**': create backup of collection<br />
'**-load**': load entries from backup<br />
'**-config**': generate config file in pwd. if config exists, defaults reset.
updating config may outdate idl<br />
'**-s**': specify default collection file.
does not modify existing files. modifes / creates config file.<br />
'**-del**': delete entry<br />
'**-q**': quick delete the last entry made
