import os
import stat
import datetime as dt
import constants as c
from entrybox import TextBox


class Entry():
    'an entry to be stored in the collection'
    def __init__(self, thing_that_was_done, shortcut=None):
        self.logged_time = dt.datetime.now()
        self.recorded_datetime = self.logged_time.strftime('%c')
        self.time = self.logged_time.strftime('%-I:%M %p')
        self.date = self.logged_time.strftime('%A, %B %-d %Y')
        self.notes = None
        self.why = None
        self.thing_experienced = thing_that_was_done
        self.begin_entry(shortcut)

    def write_to(self):
        'writes entry to file, formatted with date/time first'
        # make file writeable
        # checks if file was maliciously removed mid-session
        try:
            os.chmod('journal.txt', stat.S_IRWXU)
        except FileNotFoundError:
            pass

        entries = open('journal.txt', 'a+')
        entries.writelines([str(self.recorded_datetime), '\n',
                            '------------------------', '\n',
                            self.thing_experienced, '\n',
                            '-', '\n',
                            self.notes, '\n',
                            '-', '\n',
                            self.why, '\n------------\nend_of_entry\n'+
                            '------------\n\n'])
        entries.close()

        # file back to readonly
        os.chmod('journal.txt', stat.S_IREAD)

    def begin_entry(self, which=None):
        'initializes textboxes, records input, manages call to write_to()'
        if which is None:
            input(c.NOTE)
            TextBox(self, 'note')
            input(c.WHY)
            TextBox(self, 'why')

        elif which == '-ng':
            input(c.NOTE)
            TextBox(self, 'note')

        elif which == '-nw':
            input(c.WHY)
            TextBox(self, 'why')

        elif which == '-e':
            pass

        # readability formatting
        if self.notes is None or self.notes == '':
            self.notes = 'N/A'

        if self.why is None or self.why == '':
            self.why = 'N/A'

        # call write function regardless of shortcut taken
        self.write_to()
