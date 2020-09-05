import Main.constants as c


class EntryWriter():
    'writes entries to file'

    @staticmethod
    def full_write(dt: str, title: str, first: str, second: str):
        'a full entry, including both sections'

        entries = open(c.COLLECTION_TITLE, 'a+')
        entries.writelines([dt, '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            title, '\n\n',
                            c.FIRST_MARKER, '\n',
                            first, '\n\n',
                            c.SECOND_MARKER, '\n',
                            second, '\n' + c.END_MARKER + '\n\n'])
        entries.close()

    @staticmethod
    def first_write(dt: str, title: str, first: str):
        'a first-section-only write'

        entries = open(c.COLLECTION_TITLE, 'a+')
        entries.writelines([dt, '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            title, '\n\n',
                            c.FIRST_MARKER, '\n',
                            first, '\n' + c.END_MARKER + '\n\n'])
        entries.close()

    @staticmethod
    def second_write(dt: str, title: str, second: str):
        'a second-section-only write'

        entries = open(c.COLLECTION_TITLE, 'a+')
        entries.writelines([dt, '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            title, '\n\n',
                            c.SECOND_MARKER + '\n',
                            second, '\n' + c.END_MARKER + '\n\n'])
        entries.close()

    @staticmethod
    def title_write(dt: str, title: str):
        'a write with a title only'

        entries = open(c.COLLECTION_TITLE, 'a+')
        entries.writelines([dt, '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            title, '\n',
                            c.END_MARKER + '\n\n'])
        entries.close()

    @staticmethod
    def tag_write(dt: str, title: str, tag: str):
        'a write with a tag'

        entries = open(c.COLLECTION_TITLE, 'a+')
        entries.writelines([dt, '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            '(' + tag + ')\n',
                            title, '\n',
                            c.END_MARKER + '\n\n'])
        entries.close()
