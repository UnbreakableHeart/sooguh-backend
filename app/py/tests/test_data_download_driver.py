import unittest
from unittest.mock import patch, MagicMock, PropertyMock, ANY
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from autoupdater.data_download_driver import DataDownloadDriver

class TestDataDownloadDriver(unittest.TestCase):
    
    def setUp(self):
        self.patcher = patch('autoupdater.data_download_driver.webdriver.Chrome')
        self.mock_webdriver = self.patcher.start()
        self.mock_webdriver.return_value = MagicMock(spec=WebDriver)

        # Mock the command_executor attribute
        command_executor_mock = MagicMock()
        type(self.mock_webdriver.return_value).command_executor = PropertyMock(return_value=command_executor_mock)
        
        # Mock the _commands dictionary on command_executor
        command_executor_mock._commands = {}

        self.driver = DataDownloadDriver()

    def tearDown(self):
        self.driver.__del__()
        self.patcher.stop()

    def test_init(self):
        self.mock_webdriver.assert_called_once()
        options = self.mock_webdriver.call_args[1]['options']
        self.assertTrue(isinstance(options, Options))
        self.assertIn('headless', options.arguments)

    def test_open_url(self):
        test_url = "http://test.com"
        self.driver.open_url(test_url)
        self.driver.driver.get.assert_called_with(test_url)

    @patch('autoupdater.data_download_driver.WebDriverWait.until')
    def test_download_data(self, mock_wait):
        mock_wait.click.return_value = True

        test_xpath = "//button[@id='download']"
        self.driver.download_data(test_xpath)
        WebDriverWait(self.driver.driver, 10).until.assert_called_once()

    def test_enable_background_download(self):
        self.driver.driver.execute.assert_called_once_with('send_command', ANY)

if __name__ == '__main__':
    unittest.main()