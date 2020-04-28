journal manager is a cli tool used to create and manage journal entries.

install instructions for running from shell:\n run `sudo ln -s /dist/journal/journal /usr/local/bin`\n if necessary, sub the first path for your own personal location of the journal executable\n in the 'dist' folder\n entries are stored as 'journal.txt' in /Users/yourname

documentation:\n to run, just run 'journal' in the shell from any directory

optional sys arguements:\n '-e': new entry, title only\n '-n': new entry with both a notes and a why section\n '-ng': new entry with a notes section\n '-nw': new entry with a why section\n

alternatively, journal.py can be run, and journal entries will be maintained in the folder