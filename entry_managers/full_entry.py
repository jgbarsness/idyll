from entry_managers.ab_entry import AEntry
from constants import constants as c
from entry_managers.entrybox import TextBox
import entry_managers.entry_writer


class FullEntry(AEntry):
    'represents a fully populated entry'

    def __init__(self, passed_title):
        super().__init__(passed_title)
        self.first = None
        self.second = None
        self.writer = entry_writer.FullWrite()
        self.begin_entry()

    def begin_entry(self):
        super().begin_entry()
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

    def format_readability(self):
        super().format_readability()
        if self.first is None or self.first == '':
            self.first = 'N/A'
        if self.second is None or self.second == '':
            self.second = 'N/A'

    def write(self):
        self.writer.write(self)
