import os
import stat
import datetime as dt
import constants as c
from entrybox import TextBox


class Entry():
    'an entry to be stored in the collection'
    def __init__(self, thing_that_was_done, shortcut=None):
        self.logged_time = dt.datetime.now()
        self.recorded_datetime = self.logged_time.strftime('%a %I:%M%p %b %d %Y')
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
            os.chmod(c.JOURNAL_TITLE, stat.S_IRWXU)
        except FileNotFoundError:
            pass

        entries = open(c.JOURNAL_TITLE, 'a+')
        if self.notes != 'N/A' and self.why != 'N/A':
            entries.writelines([str(self.recorded_datetime), '\n',
                                c.DATESTAMP_UNDERLINE, '\n',
                                self.thing_experienced, '\n',
                                c.NOTES_MARKER, '\n',
                                self.notes, '\n',
                                c.WHY_MARKER, '\n',
                                self.why, '\n' + c.END_MARKER + '\n\n'])
            entries.close()

        elif self.notes == 'N/A' and self.why != 'N/A':
            entries.writelines([str(self.recorded_datetime), '\n',
                                c.DATESTAMP_UNDERLINE, '\n',
                                self.thing_experienced, '\n',
                                c.WHY_MARKER + '\n',
                                self.why, '\n' + c.END_MARKER + '\n\n'])
            entries.close()

        elif self.why == 'N/A' and self.notes != 'N/A':
            entries.writelines([str(self.recorded_datetime), '\n',
                                c.DATESTAMP_UNDERLINE, '\n',
                                self.thing_experienced, '\n',
                                c.NOTES_MARKER, '\n',
                                self.notes, '\n' + c.END_MARKER + '\n\n'])
            entries.close()

        else:
            entries.writelines([str(self.recorded_datetime), '\n',
                                c.DATESTAMP_UNDERLINE, '\n',
                                self.thing_experienced, '\n',
                                c.END_MARKER + '\n\n'])
            entries.close()

        # file back to readonly
        os.chmod(c.JOURNAL_TITLE, stat.S_IREAD)

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
