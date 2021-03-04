from peck.ab_entry import AEntry
import peck.info_and_paths as c
import peck.entry_writer


class FullEntry(AEntry):
    'represents a fully populated entry'

    def __init__(self, passed_title):
        super().__init__(passed_title)
        self.first = None
        self.second = None
        self.writer = peck.entry_writer.FullWrite()
        self.begin_entry()

    def begin_entry(self):
        from peck.entrybox import TextBox
        super().begin_entry()
        # indicates the user wants to not create a new file
        if self.print is False:
            return
        if c.USE_TEXTBOX is False:
            self.first = input(c.FIRST_NT)
            self.second = input(c.SECOND_NT)
        else:
            input(c.FIRST)
            TextBox(self, 'first')
            input(c.SECOND)
            TextBox(self, 'second')
        # format and call write
        self.format_readability()

    def format_readability(self):
        super().format_readability()
        if self.first is None or self.first == '':
            self.first = 'N/A'
        if self.second is None or self.second == '':
            self.second = 'N/A'

    def write(self):
        self.writer.write(self)
