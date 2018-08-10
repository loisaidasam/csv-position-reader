
import os.path
import unittest

import csv_position_reader


DIR_TESTS = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(DIR_TESTS, 'data')
FILENAME_BASIC = os.path.join(DIR_DATA, 'basic.csv')


class ReaderTests(unittest.TestCase):
    def test_basic(self):
        with open(FILENAME_BASIC, 'r') as fp:
            reader = csv_position_reader.reader(fp)
            row = reader.next()
            self.assertEqual(row, (0, ['name', 'favorite_color', 'city']))
            position, data = row
            self.assertTrue(isinstance(position, int))
            row = reader.next()
            self.assertEqual(row, (26, ['Sam', 'black', 'Atlanta']))
            row = reader.next()
            self.assertEqual(row, (45, ['Vaughn', 'blue', 'Atlanta']))
            row = reader.next()
            self.assertEqual(row, (66, ['James', 'pink', 'Brooklyn']))
            row = reader.next()
            self.assertEqual(row, (87, ['Rok', 'green', 'Ljubljana']))
            with self.assertRaises(StopIteration):
                reader.next()

    def test_seek(self):
        with open(FILENAME_BASIC, 'r') as fp:
            reader = csv_position_reader.reader(fp)
            reader.seek(66)
            row = reader.next()
            self.assertEqual(row, (66, ['James', 'pink', 'Brooklyn']))

    def test_bad_seek(self):
        with open(FILENAME_BASIC, 'r') as fp:
            reader = csv_position_reader.reader(fp)
            reader.seek(75)
            row = reader.next()
            # TODO: Is there anything we can do here?
            self.assertEqual(row, (75, ['k', 'Brooklyn']))


class DictReaderTests(unittest.TestCase):
    def test_basic(self):
        with open(FILENAME_BASIC, 'r') as fp:
            reader = csv_position_reader.DictReader(fp)
            row = reader.next()
            row_expected = (
                26,
                {'city': 'Atlanta', 'favorite_color': 'black', 'name': 'Sam'},
            )
            self.assertEqual(row, row_expected)
            position, data = row
            self.assertTrue(isinstance(position, int))
            row = reader.next()
            row_expected = (
                45,
                {'city': 'Atlanta', 'favorite_color': 'blue', 'name': 'Vaughn'},
            )
            self.assertEqual(row, row_expected)
            row = reader.next()
            row_expected = (
                66,
                {'city': 'Brooklyn', 'favorite_color': 'pink', 'name': 'James'},
            )
            self.assertEqual(row, row_expected)
            row = reader.next()
            row_expected = (
                87,
                {'city': 'Ljubljana', 'favorite_color': 'green', 'name': 'Rok'},
            )
            self.assertEqual(row, row_expected)
            with self.assertRaises(StopIteration):
                reader.next()

    def test_seek_without_setting_header(self):
        with open(FILENAME_BASIC, 'r') as fp:
            reader = csv_position_reader.DictReader(fp)
            with self.assertRaises(csv_position_reader.HeaderNotSetError):
                reader.seek(66)

    def test_seek(self):
        with open(FILENAME_BASIC, 'r') as fp:
            reader = csv_position_reader.DictReader(fp)
            reader.set_header()
            reader.seek(66)
            row = reader.next()
            row_expected = (
                66,
                {'city': 'Brooklyn', 'favorite_color': 'pink', 'name': 'James'},
            )
            self.assertEqual(row, row_expected)

    def test_bad_seek(self):
        with open(FILENAME_BASIC, 'r') as fp:
            reader = csv_position_reader.DictReader(fp)
            reader.set_header()
            reader.seek(75)
            row = reader.next()
            # TODO: Is there anything we can do here?
            row_expected = (
                75,
                {'favorite_color': 'Brooklyn', 'name': 'k'},
            )
            self.assertEqual(row, row_expected)
