import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from autoupdater.util.conf import config
from autoupdater.util import logger
from autoupdater.DataPortalSearcher import DataPortalSearcher
import requests

class TestDataPortalSearcher(unittest.TestCase):
    log = logger.get_logger(__name__)
    searcher = DataPortalSearcher()

    TEST_HTML_RESPONSE_OK = """
        <div class='result-list'><ul>
            <li>
                <span class='title'>Title1</span>
                    <div class='info-data'>
                        <p><span class='data'>Provider1</span></p>
                        <p><span class='data'>Date1</span></p>
                    </div>
                </span>
            </li>
            <li>
                <span class='title'>Title2</span>
                    <div class='info-data'>
                        <p><span class='data'>Provider2</span></p>
                        <p><span class='data'>Date2</span></p>
                    </div>
                </span>
            </li>
        </ul></div>
    """  

    TEST_HTML_RESPONSE_NO_RESULT = """
        <div class='result-list'><ul>
            <div class="no-list">
				<p class="txt">	검색 결과가 없습니다.</p>
				<p class="no-data-txt"> 검색어를 다시 한번 더 확인해 주세요.</p>
			</div>
        </ul></div>
    """   

    TEST_HTML_RESPONSE_FAIL_LENGTH = """
        <div class='result-list'><ul>
            <li>
                <span class='title'>Title1</span>
                    <div class='info-data'>
                        <p><span class='data'>Provider1</span></p>
                    </div>
                </span>
            </li>
        </ul></div>
    """    
    

    @patch('requests.get')
    def test_get_info_list_http_exception1(self, mock_get):
        self.log.info(f"Test Start: test_get_info_list_http_exception1")
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Not Found"

        with self.assertRaises(Exception) as context:
            self.searcher._get_info_list("http://example.com")

        self.assertEqual(str(context.exception), "HTTP error: 404")

    @patch('requests.get')
    def test_get_info_list_http_exception2(self, mock_get):
        self.log.info(f"Test Start: test_get_info_list_http_exception2")
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = "Internal Server Error"

        with self.assertRaises(Exception) as context:
            self.searcher._get_info_list("http://example.com")

        self.assertEqual(str(context.exception), "HTTP error: 500")

    @patch('requests.get')
    def test_get_info_list_length_exception1(self, mock_get):
        self.log.info(f"Test Start: test_get_info_list_length_exception1")
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = self.TEST_HTML_RESPONSE_FAIL_LENGTH
        
        with self.assertRaises(Exception) as context:
            self.searcher._get_info_list("http://example.com")
        self.assertEqual(str(context.exception), "title, provider, date length is not equal")

    @patch('requests.get')
    def test_get_info_list_correct(self, mock_get):
        self.log.info(f"Test Start: test_get_info_list_length_exception1")
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = self.TEST_HTML_RESPONSE_OK
        
        result = self.searcher._get_info_list("http://example.com")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], 'Title1')
        self.assertEqual(result[0]['provider'], 'Provider1')
        self.assertEqual(result[0]['date'], 'Date1')
        self.assertEqual(result[1]['title'], 'Title2')
        self.assertEqual(result[1]['provider'], 'Provider2')
        self.assertEqual(result[1]['date'], 'Date2')

    @patch('requests.get')
    def test_get_info_list_no_results(self, mock_get):
        self.log.info(f"Test Start: test_get_info_list_no_results")
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = self.TEST_HTML_RESPONSE_NO_RESULT
        
        result = self.searcher._get_info_list("http://example.com")
        self.assertEqual(len(result), 0)

    def test_get_info_lists_correct(self):
        self.log.info(f"Test Start: test_get_info_lists_correct")
        keyword = config['SEARCH_CONFIG']['SEARCH_KEYWORD'][0]
        result = self.searcher.get_info_lists(keyword)
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)

    def test_get_info_lists_invalid_keyword(self):
        self.log.info(f"Test Start: test_get_info_lists_correct")
        keyword = 'invalid_keyword'
        result = self.searcher.get_info_lists(keyword)
        self.assertIsNotNone(result)
        self.assertTrue(len(result) == 0)

if __name__ == '__main__':
    unittest.main()