from entry_managers.ab_entry import AEntry
from constants import info_and_paths as c
from entry_managers.entrybox import TextBox
from entry_managers import entry_writer


class TitleEntry(AEntry):
    'represents a title-only entry'

    def __init__(self, passed_title, force=False):
        super().__init__(passed_title)
        self.force = force
        self.writer = entry_writer.TitleWrite()
        self.begin_entry()

    def begin_entry(self):
        super().begin_entry()
        # indicates the user wants to not create a new file
        if self.print is False:
            return
        # if textbox use is forced
        if self.force:
            TextBox(self, 'title')
        self.format_readability()

    def write(self):
        self.writer.write(self)

    def format_readability(self):
        super().format_readability()
