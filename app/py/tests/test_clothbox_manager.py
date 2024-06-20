import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from autoupdater.clothbox_manager import ClothBoxManager
from datetime import datetime

class TestClothBoxManager(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('autoupdater.clothbox_manager.pymongo.MongoClient')
        self.mock_client = self.patcher.start()

        self.mock_db = MagicMock()
        self.mock_client.return_value.__getitem__.return_value = self.mock_db
        self.mock_collection = MagicMock()
        self.mock_db.__getitem__.return_value = self.mock_collection

        self.manager = ClothBoxManager()

    def tearDown(self):
        self.patcher.stop()
        pass

    def test_read_last_update_date(self):
        self.mock_collection.find.return_value.sort.return_value.limit.return_value = [{'update_date': datetime(2020, 1, 1)}]
        result = self.manager.read_last_update_date()
        self.assertEqual(result, datetime(2020, 1, 1))

    def test_write_update_info(self):
        self.mock_collection.update_one.return_value = type('obj', (object,), {'acknowledged': True})
        result = self.manager.write_update_info(['Suwon'])
        self.assertTrue(result)

    def test_write_clothbox_data(self):
        self.mock_collection.update_one.return_value = type('obj', (object,), {'acknowledged': True})
        result = self.manager.write_clothbox_data("Suwon", "수원", [37.5665, 126.9780])
        self.assertTrue(result)

    def test_get_clothbox_data(self):
        self.mock_collection.find.return_value = [{'address': 'Suwon'}]
        result = self.manager.get_clothbox_data("수원")
        self.assertEqual(result, ['Suwon'])

    def test_delete_clothbox_data(self):
        self.mock_collection.delete_one.return_value = type('obj', (object,), {'acknowledged': True})
        result = self.manager.delete_clothbox_data("Suwon")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()