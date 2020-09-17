from entry_managers.ab_entry import AEntry
from constants import constants as c
from entry_managers.entrybox import TextBox
from entry_managers import entry_writer


class SecondEntry(AEntry):
    'represents an entry with a second section'

    def __init__(self, passed_title):
        super().__init__(passed_title)
        self.second = None
        self.writer = entry_writer.SecondWrite()
        self.begin_entry()

    def begin_entry(self):
        super().begin_entry()
        if self.print is False:
            return
        if c.USE_TEXTBOX is False:
            self.second = input(c.SECOND_NT)
        else:
            input(c.SECOND)
            TextBox(self, 'second')
        self.format_readability()

    def write(self):
        self.writer.write(self)

    def format_readability(self):
        super().format_readability()
        if self.second is None or self.second == '':
            self.second = 'N/A'
