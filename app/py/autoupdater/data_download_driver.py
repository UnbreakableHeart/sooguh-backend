"""Downloading files from the specified URL to the specified  path using Selenium WebDriver.

This module is used to download files from the specified URL to the specified path using Selenium WebDriver.

Example:
    >>> driver = DataDownloadDriver()
    >>> driver.open_url(f'{url}')
    >>> driver.download_data(f'{xpath})  

"""

import sys
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
from autoupdater.util.logger import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
import time
import os
import platform

log = Logger.get_instance(__name__)

class DataDownloadDriver():
        """A class for downloading files from the specified URL

        Attributes:
            DOWNLOAD_PATH (str): The path to download the file.
            driver (webdriver): A WebDriver instance for downloading files.

        Mehtods:
            open_url(url: str) -> None: Opens the specified URL.
            download_data(xpath: str) -> str: Downloads the file using the specified xpath.
        """
        DOWNLOAD_PATH = os.getcwd() + "\\res"

        def __init__(self) -> None:
            
            log.info("Initializing driver")
            options = webdriver.ChromeOptions()
            # 백그라운드 실행 옵션 추가
            options.add_argument("headless")
            options.add_argument("window-size=1920x1080")
            if platform.system() == "Linux" and "Ubuntu" in platform.release():
                self.driver = webdriver.Chrome(executable_path=os.getcwd() +'\\bin\\chromedriver', options=options)
            else:
                self.driver = webdriver.Chrome(options=options)
            self._enable_background_download()
            
            return
        
        def open_url(self, url: str) -> None:
            """Opens the specified URL.

            Args:
                url (str): The URL to open.
            """

            log.info(f"Openning url: {url}")
            self.driver.get(url)
            return
        
        def download_data(self, xpath: str) -> None:
            """Downloads the file using the specified xpath.

            Args:
                xpath (str): The xpath to download the file.
            """
            log.info(f"Downloading data")
            try:
                self.driver.maximize_window()
                button = WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
                button.click()
                WebDriverWait(self.driver, 10).until(expected_conditions.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
            except TimeoutException:
                log.error("Timeout: Element not clickable")
            except NoAlertPresentException:
                log.warn("No alert present after clicking the button")
            time.sleep(5)
            return
        
        def _enable_background_download(self):
            log.info(f"Enabling background download, download path: {self.DOWNLOAD_PATH}")
            self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self.DOWNLOAD_PATH}}
            self.driver.execute("send_command", params)

            return

        def __del__(self):
            self.driver.quit()
            return
        
if __name__ == "__main__":
    driver = DataDownloadDriver()
    driver.open_url('https://www.data.go.kr/data/15127178/fileData.do')
    driver.download_data('//*[@id="tab-layer-file"]/div[2]/div[2]/a')    
