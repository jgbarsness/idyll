import os
import stat
import datetime as dt
import Main.constants as c
from Entrys.entrybox import TextBox
from Entrys.entry_writer import EntryWriter


class Entry:
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

    def begin_entry(self, which=None):
        'initializes textboxes, records input, manages call to write'

        try:
            os.chmod(c.COLLECTION_TITLE, stat.S_IRWXU)
        except FileNotFoundError:
            # permission handling will be passed down if continued
            check = input("\nno collection file in pwd. create? y/n\n")
            if check != 'y':
                print("\ncollection not created")
                return

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
            # format and call write
            self.format_readability()
            EntryWriter.full_write(str(self.recorded_datetime), self.title, self.first, self.second)

        elif which == '-n1':
            if c.USE_TEXTBOX is False:
                self.first = input(c.FIRST_NT)
            else:
                input(c.FIRST)
                TextBox(self, 'first')
            self.format_readability()
            EntryWriter.first_write(str(self.recorded_datetime), self.title, self.first)

        elif which == '-n2':
            if c.USE_TEXTBOX is False:
                self.second = input(c.SECOND_NT)
            else:
                input(c.SECOND)
                TextBox(self, 'second')
            self.format_readability()
            EntryWriter.second_write(str(self.recorded_datetime), self.title, self.second)

        elif which == '-e':
            self.format_readability()
            EntryWriter.title_write(str(self.recorded_datetime), self.title)

        elif which == '-a':
            # create tag and exit function
            tag = self.title[0]
            del self.title[0]
            self.title = ' '.join(self.title)
            self.format_readability()
            EntryWriter.tag_write(str(self.recorded_datetime), self.title, tag)
        
        elif which == '-nt':
            # entry with only a textbox
            TextBox(self, 'title')
            self.format_readability()
            EntryWriter.title_write(str(self.recorded_datetime), self.title)
        
        os.chmod(c.COLLECTION_TITLE, stat.S_IREAD)
        print('\nnew entry in ' + c.PURPLE + os.path.abspath(c.COLLECTION_TITLE) + c.END +
              '\ntitled: ' + '\'' + self.title + '\'')

    def format_readability(self):
        'sets fields to "N/A" if empty'

        if self.first is None or self.first == '':
            self.first = 'N/A'

        if self.second is None or self.second == '':
            self.second = 'N/A'

        if self.title is None or self.title == '':
            self.title = 'N/A'
