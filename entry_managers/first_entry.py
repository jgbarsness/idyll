from entry_managers.ab_entry import AEntry
from constants import constants as c
from entry_managers.entrybox import TextBox
import entry_managers.entry_writer


class FirstEntry(AEntry):
    'represents an entry with a first section'

    def __init__(self, passed_title):
        super().__init__(passed_title)
        self.first = None
        self.writer = entry_writer.FirstWrite()
        self.begin_entry()

    def begin_entry(self):
        super().begin_entry()
        if c.USE_TEXTBOX is False:
            self.first = input(c.FIRST_NT)
        else:
            input(c.FIRST)
            TextBox(self, 'first')
        self.format_readability()

    def write(self):
        self.writer.write(self)

    def format_readability(self):
        super().format_readability()
        if self.first is None or self.first == '':
            self.first = 'N/A'
