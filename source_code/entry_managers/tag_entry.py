from entry_managers.ab_entry import AEntry
from constants_routers import constants as c
from entry_managers.entrybox import TextBox
from entry_managers.entry_writer import EntryWriter


class TagEntry(AEntry):
    'represents an entry with a tag'
    
    def __init__(self, passed_title, tag):
        super().__init__(passed_title)
        self.tag = tag
        self.begin_entry()

    def begin_entry(self):
        super().begin_entry()
        self.format_readability()

    def write(self):
        EntryWriter.tag_write(str(self.recorded_datetime), self.title, self.tag)

    def format_readability(self):
        super().format_readability()
