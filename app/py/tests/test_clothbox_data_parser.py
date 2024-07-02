import unittest
from unittest.mock import patch
import pandas as pd
from io import StringIO
import sys
import os
sys.path.append(os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ))
from autoupdater.clothbox_data_parser import CsvParser, ClothBoxDataParser

class TestCsvParser(unittest.TestCase):

    def setUp(self):
        self.parser = ClothBoxDataParser()
        self.parser.set_strategy(CsvParser())

    @patch('pandas.read_csv')
    def test_parse_address_valid_data_(self, mock_read_csv):
        test_data = pd.DataFrame({"상세주소": ["123 Main St", "456 Elm St"]})
        mock_read_csv.return_value = test_data
        result = self.parser.parse_address('dummy_path.csv')
        self.assertEqual(result, ['123 Main St', '456 Elm St'])

    @patch('pandas.read_csv')
    def test_parse_address_different_encodings(self, mock_read_csv):
        test_data_utf8 = pd.DataFrame({"위치": ["123 Main St"]})
        mock_read_csv.side_effect = [UnicodeDecodeError('utf-8', b"", 0, 1, 'invalid start byte'), test_data_utf8]
        result = self.parser.parse_address('dummy_path.csv')
        self.assertEqual(result, ['123 Main St'])

    @patch('pandas.read_csv')
    def test_parse_address_missing_index_column(self, mock_read_csv):
        test_data = pd.DataFrame({"NotAddress": ["123 Main St"]})
        mock_read_csv.return_value = test_data
        result = self.parser.parse_address('dummy_path.csv')
        self.assertIsNone(result)

    @patch('pandas.read_csv')
    def test_parse_address_empty_file(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame()
        result = self.parser.parse_address('dummy_path.csv')
        self.assertEqual(result, None)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()