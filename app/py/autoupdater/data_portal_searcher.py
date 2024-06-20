"""Exploring the Public Data Portal and search data by keyword and date

This module is used to search data by keyword and date

Example:
    >>> searcher = DataPortalSearcher()
    >>> result = searcher.search_data('keyword')
    >>> result = searcher.search_data(f'{keyword}', f'{date}') # date format: 'YYYY-MM-DD'
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
import time


log = logger.get_logger(__name__)

class IDataPortalSearcher(metaclass=abc.ABCMeta):
    """An abstract base class for data portal searchers.

    This interface defines the methods that should be implemented by a class that search for data in a data portal.
    """
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def search_data(self, keyword:str, date:str=None) -> List[Dict[str, str]]:
        """Abstract method to search all data by a given keyword.
        
        Search data from the data portal and and returns a list of dictionaries containing information about the data found by the given keyword. 
        Each dictionary should have the following keys: 'title', 'provider', 'date', and 'link'.

        Args:
            keyword (str): The keyword to search for in the data portal.
            date (str, optional): The date to search for in the data portal. 
                It will search data if the modification date is more recent than the given date. 
                Defaults to None.(If None, it will download all data.)
                Example: '2020-01-01'

        Returns:    
            List[Dict[str, str]]: A list of dictionaries containing information about the data found by the given keyword. Each dictionary should have the following keys: 'title', 'provider', 'date', and 'link'.
                title (str): The title of the data.
                provider (str): The name of the organization that provided the information.
                date (str): The date when the data was last updated.
                link (str): The link to download the data.
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
    def search_data(self, keyword: str, date: str=None) -> List[Dict[str, str]]:
        """Search data portal using the given keyword and return the list of data.
        
        Search data from the data portal and and returns a list of dictionaries containing information about the data found by the given keyword. 
        Each dictionary should have the following keys: 'title', 'provider', 'date', and 'link'.

        Args:
            keyword (str): The keyword to search for in the data portal.
            date (str, optional): The date to search for in the data portal. 
                It will search data if the modification date is more recent than the given date. 
                Defaults to None.(If None, it will download all data.)
                Example: '2020-01-01'

        Returns:    
            List[Dict[str, str]]: A list of dictionaries containing information about the data found by the given keyword. Each dictionary should have the following keys: 'title', 'provider', 'date', and 'link'.
                title (str): The title of the data.
                provider (str): The name of the organization that provided the information.
                date (str): The date when the data was last updated.
                link (str): The link to download the data.
        """

        log.info(f"Start to search by keyword: {keyword}")
        result = []
        
        self.search_params['keyword'] = keyword
        page = 1
        if date != None:
            date = time.strptime(date, "%Y-%m-%d")

        try:
            while True:
                self.search_params['currentPage'] = str(page)
                url = self.SEARCH_CONFIG['SEARCH_BASE_URL'] + urlencode(self.search_params)
                ret = self._get_info_list(url)
                if not ret:
                    break

                for item in ret:
                    file_date = time.strptime(item['date'], "%Y-%m-%d")
                    if date and file_date < date:
                        log.info(f"-- Skip data: {item}")
                        continue
                    log.info(f"Getting data: {item}")
                    result.append(ret)
                page += 1

        except Exception as e:
            log.error(traceback.format_exc())
            log.error(e)
            log.error(f"Failed to search")
        
        return result
    
    def _get_info_list(self, url: str) -> Tuple[List[Dict[str, str]], List[str]]:
        log.info(f"Start to get info list form {url}")
        response = requests.get(url)
        result= []

        if response.status_code == config['WEB_STATUS']['OK']:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            ul = soup.select_one(self.SEARCH_CONFIG['SEARCH_LIST_SELECTOR'])

            if ul is None:
                log.info("No search results")
                return result

            titles = ul.select(self.SEARCH_CONFIG['TITLE_SELECTOR'])
            providers = ul.select(self.SEARCH_CONFIG['PROVIDER_SELECTOR'])
            dates = ul.select(self.SEARCH_CONFIG['MODIFIED_DATE_SELECTOR'])
            download_links = ul.select(self.SEARCH_CONFIG['ITEM_LINK_SELECTOR'])

            if len(titles) == len(providers) == len(dates) == len(download_links):
                log.info("Succeed to get info list")
                for title, provider, date, link in zip(titles, providers, dates, download_links):
                    result.append({
                        'title': title.get_text().strip(),
                        'provider': provider.get_text().strip(),
                        'date': date.get_text().strip(),
                        'link': link['href']
                    })
            else:
                raise Exception("title, provider, date length is not equal")
        else:
            raise Exception(f"HTTP error: {response.status_code}")
        
        return result
    
if __name__ == "__main__":
    search = DataPortalSearcher()
    result = search.search_data(config['SEARCH_CONFIG']['SEARCH_KEYWORD'][0])
    print(len(result))
    result = search.search_data(config['SEARCH_CONFIG']['SEARCH_KEYWORD'][1], '2024-06-01')
    print(len(result))