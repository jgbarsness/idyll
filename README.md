## idyll <br />
is a command line tool that allows you to take notes across directories without cluttering your work spaces.<br />
to install, download source and run:<br />
```sudo ln -s [your path to bin/[OS]/pck] /usr/local/bin```
#### using:

```pck [command] [keyword (if appropriate)]```<br />
or for a quick entry:<br />
```pck [entry]```

#### how everything works:

notes are formatted as follows:<br />
```
Sat 04:48PM Sep 19 2020
-----------------------
this is an idyll note
#*#*#*#*#*#*#*#*#*#*#*#
``` 
 
each file can contain any number of notes.

all of your notes are stored in your home directory in a folder called ```pck```. when you run idyll from a new location, a folder is created inside ```pck``` that references this location. for example, if your shell points to ```You/Desktop```, running ```pck [note]``` will add an entry to a ```You_Desktop``` folder in ```home/pck```. idyll recognizes the directory from where you are taking notes, but leaves the location itself untouched. this allows you to take notes without the worry of cluttering your work spaces.

to create a new collection file, run a command. default is ```pck.txt```, or you can run ```pck -s [new_name]``` to set a new default name. ```pck -s [name]``` can also be used to create a new collection file on next note. running ```pck -l``` will print a header with useful information on files in your ```pck``` folder.

config attributes allow various changes to how idyll formats your notes. this file is generated with ```pck -config```, or when ```pck -s [new file]``` is run. for example, if you want the date header to be underlined differently, this attribute can be modified. if you want a different string to mark the end of an entry, this can be modified. it should be noted that changing things integral to how the program functions, such as an entry end marker, will outdate the directory you are working in. specifications on what is safe to update in an existing directory are included in the config file itself (pck.ini).

suggestions for use: to-do list, dream journal, version note manager, recipe experimentation database, anything that you want to keep track of paired with the time you remembered to record it

#### commands:

'**-n**': new entry with both first and second sections<br />
'**-n1**': new entry with first section<br />
'**-n2**': new entry with second section<br />
'**-nt**': new entry using a textbox. ignores config file preferences<br />
'**-a**': new tagged entry. syntax: pck -a [tag] [entry]<br />
'**-v**': view entries. syntax: pck -v // pck -v [keyword]<br />
'**-vf**': view a difference collection in the same directory. format: 'pck -vf: [collection name][opt keyword]'<br />
'**-ds**': view entries on a specific date. format: 'pck -ds [mm/dd/yy]'<br />
'**-t**': search for entries with a tag<br />
'**-wipe**': delete current default<br />
'**-wipe-all**': delete folder referencing this location<br />
'**-b**': create backup of collection<br />
'**-load**': load entries from backup<br />
'**-config**': generate config file in pwd. if config exists, defaults reset.
updating config may outdate pck<br />
'**-s**': specify default collection file.
does not modify existing files. modifes / creates config file.<br />
'**-del**': delete entry<br />
'**-q**': quick delete the last entry made<br />

#### build with pyinstaller:
1.) pyinstaller [options] `__main__.py` <br />
2.) (optional) copy ```google_api_python_client-1.12.1.dist-info``` folder to ```[project]/bin/[os]/[pck]``` directory to allow for google drive support (note: not implemented in current builds / source. check issue #3 for more information)
