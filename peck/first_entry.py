from peck.ab_entry import AEntry
import peck.info_and_paths as c
import peck.entry_writer


class FirstEntry(AEntry):
    'represents an entry with a first section'

    def __init__(self, passed_title):
        super().__init__(passed_title)
        self.first = None
        self.writer = peck.entry_writer.FirstWrite()
        self.begin_entry()

    def begin_entry(self):
        from peck.entrybox import TextBox
        super().begin_entry()
        # indicates the user wants to not create a new file
        if self.print is False:
            return
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
