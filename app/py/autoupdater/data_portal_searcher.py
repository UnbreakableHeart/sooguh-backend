"""Exploring the Public Data Portal and download data by keyword and date

This module is used to download data by keyword and date

Example:
    >>> searcher = DataPortalSearcher()
    >>> result = searcher.download_data('keyword')
    >>> result = searcher.download_data(f'{keyword}', f'{date}') # date format: 'YYYY-MM-DD'
"""

import sys
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
from autoupdater.util import logger
from autoupdater.util.conf import config
import abc
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import traceback
from overrides import overrides
from typing import List, Dict, Tuple
from data_download_driver import DataDownloadDriver
import time

log = logger.get_logger(__name__)

class IDataPortalSearcher:
    """An abstract base class for data portal searchers.

    This interface defines the methods that should be implemented by a class that search for data in a data portal.
    """
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def download_data(self, keyword:str, date:str=None) -> List[Dict[str, str]]:
        """Abstract method to download all data by a given keyword.
        
        Download data from the data portal and and returns a list of dictionaries containing information about the data found by the given keyword. 
        Each dictionary should have the following keys: 'title', 'provider', 'date', and 'filename'.
        """
        pass

class DataPortalSearcher(IDataPortalSearcher): 
    """A class for searching data in a data portal.

    Attributes:
        SEARCH_CONFIG (dict): Configuration parameters for the search.
        search_params (dict): Parameters for the search query.            
    """

    SEARCH_CONFIG = config['SEARCH_CONFIG']
    search_params = {
            'dType': 'FILE',
            'keyword': '',
            'operator': 'AND',
            'recmSe': 'N',
            'sort': 'updtDt',
            'currentPage': '',
            'perPage': SEARCH_CONFIG['SEARCH_PER_PAGE']
        }
        
    def __init__(self) -> None:
        super().__init__()
        return
    
    @overrides
    def download_data(self, keyword: str, date: str=None) -> List[Dict[str, str]]:
        """Download data portal using the given keyword and return the list of data.

        Download data from the data portal and and returns a list of dictionaries containing information about the data found by the given keyword. 
        Each dictionary should have the following keys: 'title', 'provider', 'date', and 'filename'.

        Args:
            keyword (str): The keyword to search for in the data portal.
            date (str, optional): The date to search for in the data portal. 
                It will download data if the modification date is more recent than the given date. 
                Defaults to None.(If None, it will download all data.)
                Example: '2020-01-01'

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing information about the data found by the given keyword. Each dictionary should have the following keys: 'title', 'provider', 'date', and 'link'.
                title (str): The title of the data.
                provider (str): The name of the organization that provided the information.
                date (str): The date when the data was last updated.
        """

        log.info(f"Start to search by keyword: {keyword}")
        result = []
        
        self.search_params['keyword'] = keyword
        page = 1
        if date != None:
            date = time.strptime(date, "%Y-%m-%d")
        
        downloader = DataDownloadDriver()

        try:
            while True:
                self.search_params['currentPage'] = str(page)
                url = self.SEARCH_CONFIG['SEARCH_BASE_URL'] + urlencode(self.search_params)
                ret, download_xpaths = self._get_info_list(url)
                if not ret:
                    break

                downloader.open_url(url)
                for i, xpath in enumerate(download_xpaths):
                    file_date = time.strptime(ret[i]['date'], "%Y-%m-%d")
                    if date and file_date < date:
                        log.info(f"Skip downloading data: {ret[i]}")
                        continue
                    log.info(f"Downloading data: {ret[i]}")
                    downloader.download_data(xpath)

                result.extend(ret)
                page += 1

        except Exception as e:
            log.error(traceback.format_exc())
            log.error(e)
            log.error(f"Failed to download")
        
        return result
    
    def _get_info_list(self, url: str) -> Tuple[List[Dict[str, str]], List[str]]:
        log.info(f"Start to get info list form {url}")
        response = requests.get(url)
        result= []
        download_xpaths = []

        if response.status_code == config['WEB_STATUS']['OK']:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            ul = soup.select_one(self.SEARCH_CONFIG['SEARCH_LIST_SELECTOR'])

            titles = ul.select(self.SEARCH_CONFIG['TITLE_SELECTOR'])
            providers = ul.select(self.SEARCH_CONFIG['PROVIDER_SELECTOR'])
            dates = ul.select(self.SEARCH_CONFIG['MODIFIED_DATE_SELECTOR'])
            download_buttons = ul.select(self.SEARCH_CONFIG['DOWNLOAD_BUTTON_SELECTOR'])

            if len(titles) == len(providers) == len(dates) == len(download_buttons):
                log.info("Succeed to get info list")
                for title, provider, date, button in zip(titles, providers, dates, download_buttons):
                    result.append({
                        'title': title.get_text().strip(),
                        'provider': provider.get_text().strip(),
                        'date': date.get_text().strip(),
                    })
                    download_xpaths.append(self._get_xpath(button))
                    log.info(result[-1]) 
                    log.info(download_xpaths[-1])
            else:
                raise Exception("title, provider, date length is not equal")
        else:
            raise Exception(f"HTTP error: {response.status_code}")
        
        return result, download_xpaths

    def _get_xpath(self, element: object) -> str:
        components = []
        child = element if element.name else element.parent
        while child is not None and child.parent is not None:
            siblings = child.parent.find_all(child.name, recursive=False)
            index = siblings.index(child) + 1
            if child.name != 'link':
                components.append(f"{child.name}[{index}]")
            child = child.parent
        components.reverse()
        return '/' + '/'.join(components)
    
if __name__ == "__main__":
    search = DataPortalSearcher()
    # result = search.download_data(config['SEARCH_CONFIG']['SEARCH_KEYWORD'][0])
    # print(len(result))
    result = search.download_data(config['SEARCH_CONFIG']['SEARCH_KEYWORD'][1], '2024-06-01')
    print(len(result))