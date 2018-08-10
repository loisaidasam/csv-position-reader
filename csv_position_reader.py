"""
A custom CSV reader implementation for specific file access.

The default builtin `csv` lib uses a read-ahead buffer on the file pointer,
making `fp.tell()` yield inaccurate results.

Some references:

https://stackoverflow.com/questions/14145082/file-tell-inconsistency/14145118#14145118
https://stackoverflow.com/questions/19151/build-a-basic-python-iterator/24377#24377
https://stackoverflow.com/questions/12109622/how-to-know-the-byte-position-of-a-row-of-a-csv-file-in-python/12110160#12110160
"""

import csv


class reader(object):
    """Like `csv.reader`, but yield successive pairs of:

    (
        <int> file position,
        <list> row,
    )

    https://docs.python.org/2/library/csv.html
    """
    def __init__(self, csvfile, dialect='excel', **fmtparams):
        self.fp = csvfile
        self.dialect = dialect
        self.fmtparams = fmtparams
        self.line_iterator = iter(self.fp.readline, '')

    def __iter__(self):
        return self

    def seek(self, position):
        self.fp.seek(position)

    def _get_csv_row_from_line(self, line):
        return csv.reader([line], self.dialect, **self.fmtparams).next()

    def _get_next_row(self):
        line = self.line_iterator.next()
        return self._get_csv_row_from_line(line)

    def next(self):
        position = self.fp.tell()
        row = self._get_next_row()
        return position, row


class DictReader(reader):
    """Like `csv.DictReader`, but yield successive pairs of:

    (
        <int> file position,
        <dict> row,
    )
    """
    def __init__(self, f, fieldnames=None, restkey=None, restval=None,
                 dialect='excel', *args, **kwds):
        super(DictReader, self).__init__(f, dialect, *args, **kwds)
        # TODO: Implement fieldnames/restkey/restval

    def set_header(self):
        self.seek(0)
        self.header = self._get_next_row()

    def _get_next_row_dict(self):
        row = self._get_next_row()
        return dict(zip(self.header, row))

    def next(self):
        if not self.header:
            self.set_header()
        position = self.fp.tell()
        row_dict = self._get_next_row_dict()
        return position, row_dict
