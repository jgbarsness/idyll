from peck.ab_entry import AEntry
import peck.entry_writer
import peck.info_and_paths as c


class SecondEntry(AEntry):
    'represents an entry with a second section'

    def __init__(self, passed_title):
        super().__init__(passed_title)
        self.second = None
        self.writer = peck.entry_writer.SecondWrite()
        self.begin_entry()

    def begin_entry(self):
        from peck.entrybox import TextBox
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
