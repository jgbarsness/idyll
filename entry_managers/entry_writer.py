import constants.constants as c
import os
import stat
from abc import ABC, abstractmethod
from entry_managers import ab_entry


class EntryWriter(ABC):
    'writes entries to file'

    @abstractmethod
    def write(self, obj: ab_entry.AEntry):
        pass


class FullWrite(EntryWriter):
    'writes a full entry to file'

    def write(self, obj):
        entries = open(c.COLLECTION_TITLE, 'a+')
        entries.writelines([obj.recorded_datetime, '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            obj.title, '\n\n',
                            c.FIRST_MARKER, '\n',
                            obj.first, '\n\n',
                            c.SECOND_MARKER, '\n',
                            obj.second, '\n' + c.END_MARKER + '\n\n'])
        entries.close()
        os.chmod(c.COLLECTION_TITLE, stat.S_IREAD)


class FirstWrite(EntryWriter):
    'a first-section-only write'

    def write(self, obj):
        entries = open(c.COLLECTION_TITLE, 'a+')
        entries.writelines([obj.recorded_datetime, '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            obj.title, '\n\n',
                            c.FIRST_MARKER, '\n',
                            obj.first, '\n' + c.END_MARKER + '\n\n'])
        entries.close()
        os.chmod(c.COLLECTION_TITLE, stat.S_IREAD)


class SecondWrite(EntryWriter):
    'a second-section-only write'

    def write(self, obj):
        entries = open(c.COLLECTION_TITLE, 'a+')
        entries.writelines([obj.recorded_datetime, '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            obj.title, '\n\n',
                            c.SECOND_MARKER + '\n',
                            obj.second, '\n' + c.END_MARKER + '\n\n'])
        entries.close()
        os.chmod(c.COLLECTION_TITLE, stat.S_IREAD)


class TitleWrite(EntryWriter):
    'a write with a title only'

    def write(self, obj):
        entries = open(c.COLLECTION_TITLE, 'a+')
        entries.writelines([obj.recorded_datetime, '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            obj.title, '\n',
                            c.END_MARKER + '\n\n'])
        entries.close()
        os.chmod(c.COLLECTION_TITLE, stat.S_IREAD)


class TagWrite(EntryWriter):
    'a write with a tag'

    def write(self, obj):
        entries = open(c.COLLECTION_TITLE, 'a+')
        entries.writelines([obj.recorded_datetime, '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            '(' + obj.tag + ')\n',
                            obj.title, '\n',
                            c.END_MARKER + '\n\n'])
        entries.close()
        os.chmod(c.COLLECTION_TITLE, stat.S_IREAD)