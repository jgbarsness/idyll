from entry_managers.ab_entry import AEntry
from constants_routers import constants as c
from entry_managers.entrybox import TextBox
from entry_managers.entry_writer import EntryWriter


class TitleEntry(AEntry):
    'represents a title-only entry'

    def __init__(self, passed_title, force=False):
        super().__init__(passed_title)
        self.force = force
        self.begin_entry()

    def begin_entry(self):
        super().begin_entry()
        # if textbox use is forced
        if self.force:
            TextBox(self, 'title')
        self.format_readability()

    def write(self):
        EntryWriter.title_write(str(self.recorded_datetime), self.title)

    def format_readability(self):
        super().format_readability()
