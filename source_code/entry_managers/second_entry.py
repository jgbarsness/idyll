from entry_managers.ab_entry import AEntry
from constants_routers import constants as c
from entry_managers.entrybox import TextBox
from entry_managers.entry_writer import EntryWriter


class SecondEntry(AEntry):
    'represents an entry with a second section'

    def __init__(self, passed_title):
        super().__init__(passed_title)
        self.second = None
        self.begin_entry()

    def begin_entry(self):
        super().begin_entry()
        if c.USE_TEXTBOX is False:
            self.second = input(c.SECOND_NT)
        else:
            input(c.SECOND)
            TextBox(self, 'second')
        self.format_readability()

    def write(self):
        EntryWriter.second_write(str(self.recorded_datetime), self.title, self.second)

    def format_readability(self):
        super().format_readability()
        if self.second is None or self.second == '':
            self.second = 'N/A'
