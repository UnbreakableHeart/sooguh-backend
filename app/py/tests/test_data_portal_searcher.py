import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from autoupdater.util import logger
from autoupdater.util.conf import config
from autoupdater.data_portal_searcher import DataPortalSearcher
from autoupdater.data_download_driver import DataDownloadDriver

class TestDataPortalSearcher(unittest.TestCase):

    TEST_HTML_RESPONSE_OK = """
        <div class='result-list'><ul>
            <li>
                <span class='title'>Title1</span>
                    <div class='info-data'>
                        <p><span class='data'>Provider1</span></p>
                        <p><span class='data'>2018-01-01</span></p>
                    </div>
                    <div class='bottom-area'>
                        <a href="link1"></a>
                    </div>
                </span>
            </li>
            <li>
                <span class='title'>Title2</span>
                    <div class='info-data'>
                        <p><span class='data'>Provider2</span></p>
                        <p><span class='data'>2024-01-01</span></p>
                    </div>
                    <div class='bottom-area'>
                        <a href="link2"></a>
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

    def setUp(self):
        self.searcher = DataPortalSearcher()
        self.mock_download_data = patch.object(DataDownloadDriver, 'download_data')
        self.mock_download_data.return_value = None
        self.mock_download_data.start()

        self.mock_open_url = patch.object(DataDownloadDriver, 'open_url')
        self.mock_open_url.return_value = None
        self.mock_open_url.start()
        

    def tearDown(self):
        pass

    @patch('requests.get')
    def test_get_info_list_length_exception1(self, mock_get):
        mock_get.return_value.status_code = config['WEB_STATUS']['OK']
        mock_get.return_value.text = self.TEST_HTML_RESPONSE_FAIL_LENGTH
        
        with self.assertRaises(Exception) as context:
            self.searcher._get_info_list("http://example.com")
        self.assertEqual(str(context.exception), "title, provider, date length is not equal")

    @patch('requests.get')
    def test_get_info_list_correct(self, mock_get):
        mock_get.return_value.status_code = config['WEB_STATUS']['OK']
        mock_get.return_value.text = self.TEST_HTML_RESPONSE_OK
        
        result, download_xpaths = self.searcher._get_info_list("http://example.com")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], 'Title1')
        self.assertEqual(result[0]['provider'], 'Provider1')
        self.assertEqual(result[0]['date'], '2018-01-01')
        self.assertEqual(result[1]['title'], 'Title2')
        self.assertEqual(result[1]['provider'], 'Provider2')
        self.assertEqual(result[1]['date'], '2024-01-01')
        self.assertEqual(len(download_xpaths), 2)

    @patch('requests.get')
    def test_get_info_list_no_results(self, mock_get):
        mock_get.return_value.status_code = config['WEB_STATUS']['OK']
        mock_get.return_value.text = self.TEST_HTML_RESPONSE_NO_RESULT
        
        result, download_xpaths = self.searcher._get_info_list("http://example.com")
        self.assertEqual(len(result), 0)

    @patch('requests.get')
    def test_download_data_invalid_keyword(self, mock_get):
        mock_get.return_value.status_code = config['WEB_STATUS']['OK']
        mock_get.return_value.text = self.TEST_HTML_RESPONSE_NO_RESULT
        
        result = self.searcher.download_data('invalid_keyword')
        self.assertEqual(len(result), 0)

    @patch('requests.get')
    def test_download_data_html_parsing_error(self, mock_get):
        mock_get.return_value.status_code = config['WEB_STATUS']['OK']
        mock_get.return_value.text = "<html></html>"  # Malformed HTML for the expected parsing
        
        result = self.searcher.download_data('no_results_keyword')
        self.assertEqual(len(result), 0)

    @patch.object(DataPortalSearcher, '_get_info_list')
    def test_download_data(self, mock_get_info_list):
        mock_get_info_list.side_effect = [
            (
                [
                    {'title': 'Data 1', 'provider': 'Provider 1', 'date': '2021-01-01'},
                    {'title': 'Data 2', 'provider': 'Provider 2', 'date': '2022-01-01'}
                ],
                ['xpath1', 'xpath2']
            ),
            ([], [])  # 루프를 종료시키기 위해 빈 리스트 반환
        ]

        result = self.searcher.download_data('keyword')
        self.mock_open_url.assert_called()
        self.assertEqual(self.mock_download_data.call_count, 2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], 'Data 1')
        self.assertEqual(result[1]['title'], 'Data 2')

    @patch.object(DataPortalSearcher, '_get_info_list')
    def test_download_data_by_date(self, mock_get_info_list):
        mock_get_info_list.side_effect = [
            (
                [
                    {'title': 'Data 1', 'provider': 'Provider 1', 'date': '2021-01-01'},
                    {'title': 'Data 2', 'provider': 'Provider 2', 'date': '2022-01-01'}
                ],
                ['xpath1', 'xpath2']
            ),
            ([], [])  # 루프를 종료시키기 위해 빈 리스트 반환
        ]

        result = self.searcher.download_data('keyword', '2021-12-01')
        self.mock_open_url.assert_called()
        self.mock_download_data.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], 'Data 1')
        self.assertEqual(result[1]['title'], 'Data 2')

if __name__ == '__main__':
    unittest.main()