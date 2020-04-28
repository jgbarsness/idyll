journal manager is a cli tool used to create and manage journal entries.

install instructions for running from shell:\
run `sudo ln -s /dist/journal/journal /usr/local/bin`\
if necessary, sub the first path for your own personal location of the journal executable in the 'dist' folder\
entries are stored as 'journal.txt' in /Users/yourname

documentation:\
to run, just run 'journal' in the shell from any directory

optional sys arguements:\
'-e': new entry, title only\
'-n': new entry with both a notes and a why section\
'-ng': new entry with a notes section\
'-nw': new entry with a why section

alternatively, journal.py can be run, and journal entries will be maintained in the folder directory
