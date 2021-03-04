from peck.ab_entry import AEntry
import peck.info_and_paths as c
import peck.entry_writer


class TagEntry(AEntry):
    'represents an entry with a tag'

    def __init__(self, passed_title, tag):
        from peck.entrybox import TextBox
        super().__init__(passed_title)
        self.tag = tag
        self.writer = peck.entry_writer.TagWrite()
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
