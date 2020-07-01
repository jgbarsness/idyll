import os
import stat
import datetime as dt
import constants as c
from entrybox import TextBox


class Entry():
    'an entry to be stored in the collection'
    def __init__(self, passed_title, shortcut=None):
        'accepts a title and an optional shortcut'
        self.now = dt.datetime.now()
        self.recorded_datetime = self.now.strftime('%a %I:%M%p %b %d %Y')
        self.time = self.now.strftime('%-I:%M %p')
        self.date = self.now.strftime('%A, %B %-d %Y')
        self.first = None
        self.second = None
        self.title = passed_title
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
                                self.title, '\n',
                                c.END_MARKER + '\n\n'])
            entries.close()

        elif self.first != 'N/A' and self.second != 'N/A':
            # write all
            entries.writelines([str(self.recorded_datetime), '\n',
                                c.DATESTAMP_UNDERLINE, '\n',
                                self.title, '\n\n',
                                c.FIRST_MARKER, '\n',
                                self.first, '\n\n',
                                c.SECOND_MARKER, '\n',
                                self.second, '\n' + c.END_MARKER + '\n\n'])
            entries.close()

        elif self.first == 'N/A' and self.second != 'N/A':
            # write without notes marker
            entries.writelines([str(self.recorded_datetime), '\n',
                                c.DATESTAMP_UNDERLINE, '\n',
                                self.title, '\n\n',
                                c.SECOND_MARKER + '\n',
                                self.second, '\n' + c.END_MARKER + '\n\n'])
            entries.close()

        elif self.second == 'N/A' and self.first != 'N/A':
            # write without why marker
            entries.writelines([str(self.recorded_datetime), '\n',
                                c.DATESTAMP_UNDERLINE, '\n',
                                self.title, '\n\n',
                                c.FIRST_MARKER, '\n',
                                self.first, '\n' + c.END_MARKER + '\n\n'])
            entries.close()

        else:
            # write with only title
            entries.writelines([str(self.recorded_datetime), '\n',
                                c.DATESTAMP_UNDERLINE, '\n',
                                self.title, '\n',
                                c.END_MARKER + '\n\n'])
            entries.close()

        # file back to readonly
        os.chmod(c.JOURNAL_TITLE, stat.S_IREAD)

    def begin_entry(self, which=None):
        'initializes textboxes, records input, manages call to write_to()'

        if which is None:
            if c.USE_TEXTBOX is False:
                self.first = input(c.FIRST_NT)
                self.second = input(c.SECOND_NT)
            else:
                input(c.FIRST)
                TextBox(self, 'first')
                input(c.SECOND)
                TextBox(self, 'second')

        elif which == '-n1':
            if c.USE_TEXTBOX is False:
                self.first = input(c.FIRST_NT)
            else:
                input(c.FIRST)
                TextBox(self, 'first')

        elif which == '-n2':
            if c.USE_TEXTBOX is False:
                self.second = input(c.SECOND_NT)
            else:
                input(c.SECOND)
                TextBox(self, 'second')

        elif which == '-e':
            pass

        elif which == '-a':
            # create tag and exit function
            tag = self.title[0]
            del self.title[0]
            self.title = ' '.join(self.title)
            self.write_to(tag)
            return

        # readability formatting
        if self.first is None or self.first == '':
            self.first = 'N/A'

        if self.second is None or self.second == '':
            self.second = 'N/A'

        # call write function regardless of shortcut taken
        self.write_to()
