from peck.ab_entry import AEntry
import peck.info_and_paths as c
import peck.entry_writer


class TitleEntry(AEntry):
    'represents a title-only entry'

    def __init__(self, passed_title, force=False):
        super().__init__(passed_title)
        self.force = force
        self.writer = peck.entry_writer.TitleWrite()
        self.begin_entry()

    def begin_entry(self):
        from peck.entrybox import TextBox
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
