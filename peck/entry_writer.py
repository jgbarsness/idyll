import peck.info_and_paths as c
from os import chmod
from abc import ABC, abstractmethod
import peck.ab_entry
from stat import S_IREAD


class EntryWriter(ABC):
    'writes entries to file'

    @abstractmethod
    def write(self, obj: peck.ab_entry.AEntry):
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
        chmod(c.COLLECTION_TITLE, S_IREAD)


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
        chmod(c.COLLECTION_TITLE, S_IREAD)


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
        chmod(c.COLLECTION_TITLE, S_IREAD)


class TitleWrite(EntryWriter):
    'a write with a title only'

    def write(self, obj):
        entries = open(c.COLLECTION_TITLE, 'a+')
        entries.writelines([obj.recorded_datetime, '\n',
                            c.DATESTAMP_UNDERLINE, '\n',
                            obj.title, '\n',
                            c.END_MARKER + '\n\n'])
        entries.close()
        chmod(c.COLLECTION_TITLE, S_IREAD)


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
        chmod(c.COLLECTION_TITLE, S_IREAD)
