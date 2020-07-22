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
        self.date = self.now.strftime('%B %d')
        self.first = None
        self.second = None
        self.title = passed_title
        self.begin_entry(shortcut)

    def full_write(self):
        'a full entry, including both sections'

        entries = open(c.JOURNAL_TITLE, 'a+')
        self.format_readability()
        entries.writelines([str(self.recorded_datetime), '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            self.title, '\n\n',
                            c.FIRST_MARKER, '\n',
                            self.first, '\n\n',
                            c.SECOND_MARKER, '\n',
                            self.second, '\n' + c.END_MARKER + '\n\n'])
        entries.close()

    def first_write(self):
        'a first-section-only write'

        entries = open(c.JOURNAL_TITLE, 'a+')
        self.format_readability()
        entries.writelines([str(self.recorded_datetime), '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            self.title, '\n\n',
                            c.FIRST_MARKER, '\n',
                            self.first, '\n' + c.END_MARKER + '\n\n'])
        entries.close()

    def second_write(self):
        'a second-section-only write'

        entries = open(c.JOURNAL_TITLE, 'a+')
        self.format_readability()
        entries.writelines([str(self.recorded_datetime), '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            self.title, '\n\n',
                            c.SECOND_MARKER + '\n',
                            self.second, '\n' + c.END_MARKER + '\n\n'])
        entries.close()

    def title_write(self):
        'a write with a title only'

        entries = open(c.JOURNAL_TITLE, 'a+')
        self.format_readability()
        entries.writelines([str(self.recorded_datetime), '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            self.title, '\n',
                            c.END_MARKER + '\n\n'])
        entries.close()

    def tag_write(self, tag):
        'a write with a tag'

        entries = open(c.JOURNAL_TITLE, 'a+')
        self.format_readability()
        entries.writelines([str(self.recorded_datetime), '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            '(' + tag + ')\n',
                            self.title, '\n',
                            c.END_MARKER + '\n\n'])
        entries.close()

    def begin_entry(self, which=None):
        'initializes textboxes, records input, manages call to _write()'

        try:
            os.chmod(c.JOURNAL_TITLE, stat.S_IRWXU)
        except FileNotFoundError:
            pass

        if which is None:
            # a full entry
            # check for textbox preference before routing further
            if c.USE_TEXTBOX is False:
                self.first = input(c.FIRST_NT)
                self.second = input(c.SECOND_NT)
            else:
                input(c.FIRST)
                TextBox(self, 'first')
                input(c.SECOND)
                TextBox(self, 'second')
            self.full_write()

        elif which == '-n1':
            if c.USE_TEXTBOX is False:
                self.first = input(c.FIRST_NT)
            else:
                input(c.FIRST)
                TextBox(self, 'first')
            self.first_write()

        elif which == '-n2':
            if c.USE_TEXTBOX is False:
                self.second = input(c.SECOND_NT)
            else:
                input(c.SECOND)
                TextBox(self, 'second')
            self.second_write()

        elif which == '-e':
            self.title_write()

        elif which == '-a':
            # create tag and exit function
            tag = self.title[0]
            del self.title[0]
            self.title = ' '.join(self.title)
            self.tag_write(tag)
        
        elif which == '-nt':
            # entry with only a textbox
            TextBox(self, 'title')
            self.title_write()
        
        os.chmod(c.JOURNAL_TITLE, stat.S_IREAD)

    def format_readability(self):
        'sets fields to "N/A" if empty'

        if self.first is None or self.first == '':
            self.first = 'N/A'

        if self.second is None or self.second == '':
            self.second = 'N/A'

        if self.title is None or self.title == '':
            self.title = 'N/A'
