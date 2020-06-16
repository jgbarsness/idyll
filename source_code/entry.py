import os
import stat
import datetime as dt
import constants as c
from entrybox import TextBox


class Entry():
    'an entry to be stored in the collection'
    def __init__(self, thing_that_was_done, shortcut=None):
        'accepts a title and an optional shortcut'
        self.logged_time = dt.datetime.now()
        self.recorded_datetime = self.logged_time.strftime('%a %I:%M%p'
                                                           ' %b %d %Y')
        self.time = self.logged_time.strftime('%-I:%M %p')
        self.date = self.logged_time.strftime('%A, %B %-d %Y')
        self.first = None
        self.second = None
        self.thing_experienced = thing_that_was_done
        self.begin_entry(shortcut)

    def write_to(self, tag=None):
        'writes entry to file, formatted with date/time first. checks for tag'

        # make file writeable
        # checks if file was maliciously removed mid-session
        try:
            os.chmod(c.JOURNAL_TITLE, stat.S_IRWXU)
        except FileNotFoundError:
            pass

        entries = open(c.JOURNAL_TITLE, 'a+')

        # is there a tag to include?
        if tag is not None:
            # write with tag
            entries.writelines([str(self.recorded_datetime), '\n',
                                c.DATESTAMP_UNDERLINE, '\n',
                                '(' + tag + ')\n',
                                self.thing_experienced, '\n',
                                c.END_MARKER + '\n\n'])
            entries.close()

        elif self.first != 'N/A' and self.second != 'N/A':
            # write all
            entries.writelines([str(self.recorded_datetime), '\n',
                                c.DATESTAMP_UNDERLINE, '\n',
                                self.thing_experienced, '\n\n',
                                c.FIRST_MARKER, '\n',
                                self.first, '\n\n',
                                c.SECOND_MARKER, '\n',
                                self.second, '\n' + c.END_MARKER + '\n\n'])
            entries.close()

        elif self.first == 'N/A' and self.second != 'N/A':
            # write without notes marker
            entries.writelines([str(self.recorded_datetime), '\n',
                                c.DATESTAMP_UNDERLINE, '\n',
                                self.thing_experienced, '\n\n',
                                c.SECOND_MARKER + '\n',
                                self.second, '\n' + c.END_MARKER + '\n\n'])
            entries.close()

        elif self.second == 'N/A' and self.first != 'N/A':
            # write without why marker
            entries.writelines([str(self.recorded_datetime), '\n',
                                c.DATESTAMP_UNDERLINE, '\n',
                                self.thing_experienced, '\n\n',
                                c.FIRST_MARKER, '\n',
                                self.first, '\n' + c.END_MARKER + '\n\n'])
            entries.close()

        else:
            # write with only title
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
            input(c.FIRST)
            TextBox(self, 'first')
            input(c.SECOND)
            TextBox(self, 'second')

        elif which == '-ng':
            input(c.FIRST)
            TextBox(self, 'first')

        elif which == '-nw':
            input(c.SECOND)
            TextBox(self, 'second')

        elif which == '-e':
            pass

        elif which == '-a':
            # create tag and exit function
            tag = self.thing_experienced[0]
            del self.thing_experienced[0]
            self.thing_experienced = ' '.join(self.thing_experienced)
            self.write_to(tag)
            return

        # readability formatting
        if self.first is None or self.first == '':
            self.first = 'N/A'

        if self.second is None or self.second == '':
            self.second = 'N/A'

        # call write function regardless of shortcut taken
        self.write_to()
