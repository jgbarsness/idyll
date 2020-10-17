from entry_managers.ab_entry import AEntry
from constants import info_and_paths as c
from entry_managers.entrybox import TextBox
from entry_managers import entry_writer


class TagEntry(AEntry):
    'represents an entry with a tag'

    def __init__(self, passed_title, tag):
        super().__init__(passed_title)
        self.tag = tag
        self.writer = entry_writer.TagWrite()
        self.begin_entry()

    def begin_entry(self):
        super().begin_entry()
        if self.print is False:
            return
        self.format_readability()

    def write(self):
        self.writer.write(self)

    def format_readability(self):
        super().format_readability()
