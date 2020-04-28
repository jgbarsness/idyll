journal manager is a cli tool used to create and manage journal entries.

install instructions for running from shell:<br /> run `sudo ln -s /dist/journal/journal /usr/local/bin`<br /> if necessary, sub the first path for your own personal location of the journal executable in the 'dist' folder<br /> entries are stored as 'journal.txt' in /Users/yourname

documentation:<br /> to run, just run 'journal' in the shell from any directory

optional sys arguements:<br /> '-e': new entry, title only<br /> '-n': new entry with both a notes and a why section<br /> '-ng': new entry with a notes section<br /> '-nw': new entry with a why section<br />

alternatively, journal.py can be run, and journal entries will be maintained in the folder