# csv-position-reader

A custom CSV reader implementation with direct file access

The default builtin Python `csv` lib uses an `8KB` read-ahead buffer on the file pointer, making `fp.tell()` yield inaccurate results. This library addresses that head on, explicitly passing back the file pointer position with each row, as well as allowing for direct seeking.

References:

- https://docs.python.org/2/library/csv.html
- https://stackoverflow.com/questions/14145082/file-tell-inconsistency/14145118#14145118
- https://stackoverflow.com/questions/12109622/how-to-know-the-byte-position-of-a-row-of-a-csv-file-in-python/12110160#12110160

## Usage

```python
>>> import csv_position_reader

>>> with open('tests/data/basic.csv', 'r') as fp:
...     reader = csv_position_reader.DictReader(fp)
...     position, row = reader.next()
...     print "position: %s" % position
...     print "row: %s" % row
...     reader.seek(position)
...     position_new, row_new = reader.next()
...     assert position == position_new
...     assert row == row_new
... 
position: 26
row: {'city': 'Atlanta', 'favorite_color': 'black', 'name': 'Sam'}
```

## Why? / Who Cares?

Because after poring through a CSV one time, you can now build a dictionary/cache of where each row lives for future `O(1)` access! You're now a stone's throw away from a CSV-driven database!
