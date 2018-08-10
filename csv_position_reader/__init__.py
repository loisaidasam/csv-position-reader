"""csv-position-reader

A custom CSV reader implementation with direct file access

The default builtin Python csv lib uses an 8KB read-ahead buffer on the file pointer, making fp.tell() yield inaccurate results. This library addresses that head on, explicitly passing back the file pointer position with each row, as well as allowing for direct seeking.

References:

- https://docs.python.org/2/library/csv.html
- https://stackoverflow.com/questions/14145082/file-tell-inconsistency/14145118#14145118
- https://stackoverflow.com/questions/12109622/how-to-know-the-byte-position-of-a-row-of-a-csv-file-in-python/12110160#12110160
"""

import csv


class HeaderNotSetError(Exception):
    pass


class reader(object):
    """Like `csv.reader`, but yield successive pairs of:

    (
        <int> file position,
        <list> row,
    )
    """
    fp = None
    dialect = 'excel'
    fmtparams = None
    line_iterator = None

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
    header = None

    def __init__(self, f, fieldnames=None, restkey=None, restval=None,
                 dialect='excel', *args, **kwds):
        super(DictReader, self).__init__(f, dialect, *args, **kwds)
        # TODO: Implement fieldnames/restkey/restval

    def seek(self, position, check_header_set=True):
        if check_header_set and not self.header:
            # An attempt to seek and then read with an empty `header` will lead
            # to seeking back to 0, which will render the seek useless.
            raise HeaderNotSetError
        super(DictReader, self).seek(position)

    def set_header(self):
        self.seek(0, check_header_set=False)
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
