"""Exploring the Public Data Portal and get the list of data by keyword

This module is used to get the list of data by keyword.

Example:
    >>> searcher = DataPortalSearcher()
    >>> result = searcher.get_info_lists('keyword')
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
from typing import List, Dict

class IDataPortalSearcher:
    """An abstract base class for data portal searchers.

    This interface defines the methods that should be implemented by a class that search for data in a data portal.
    """
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def get_info_lists(self, keyword:str) -> List[Dict[str, str]]:
        """Abstract method to get the list of data by a given keyword.
        
        Searches for information from the data portal and returns a list of dictionaries containing information about the data found by the given keyword. 
        Each dictionary should have the following keys: 'title', 'provider', 'date', and 'link'.

        Parameters:
            keyword (str): The keyword to search for in the data portal.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing information about the data found by the given keyword. Each dictionary should have the following keys: 'title', 'provider', 'date', and 'link'.
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
        self.log = logger.get_logger(__name__)
        return
    
    @overrides
    def get_info_lists(self, keyword: str) -> List[Dict[str, str]]:
        """ Search data portal using the given keyword and return the list of data.
        
        This method searches for all pages and all information from the data portal.
        And it returns a list of dictionaries containing information about the data found by the given keyword.

        Args:
            keyword (str): The keyword to search for in the data portal.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing information about the data found by the given keyword. Each dictionary should have the following keys: 'title', 'provider', 'date', and 'link'.
                title (str): The title of the data.
                provider (str): The name of the organization that provided the information.
                date (str): The date when the data was last updated.
                link (str): The link to the data file.
        """
        self.log.info(f"Start to search by keyword: {keyword}")
        result = []

        self.search_params['keyword'] = keyword
        page = 1
        try:
            while True:
                self.search_params['currentPage'] = str(page)
                url = self.SEARCH_CONFIG['SEARCH_BASE_URL'] + urlencode(self.search_params)
                ret = self._get_info_list(url)
                if not ret:
                    break
                result.extend(ret)
                page += 1
        except Exception as e:
            self.log.error(traceback.format_exc())
            self.log.error(e)
            self.log.error(f"Failed to get info list")
        
        return result
    
    def _get_info_list(self, url: str) -> List[Dict[str, str]]:
        """Get search results from the given data portal page and return a list of dictionaries containing information.
        
        This method searches only from the given url.

        Args:
            url (str): The URL of the data portal page to scrape.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing information about the data found by the given keyword. Each dictionary should have the following keys: 'title', 'provider', 'date', and 'link'.
                title (str): The title of the data.
                provider (str): The name of the organization that provided the information.
                date (str): The date when the data was last updated.
                link (str): The link to the data file.

        Exceptions:
            Exception: If the response status code is not 200.
            Exception: If the length of titles, providers, dates, and links are not equal.
        """
        self.log.info(f"Start to get info list form {url}")
        response = requests.get(url)
        result= []

        if response.status_code == config['WEB_STATUS']['OK']:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            ul = soup.select_one(self.SEARCH_CONFIG['SEARCH_LIST_SELECTOR'])

            titles = ul.select(self.SEARCH_CONFIG['TITLE_SELECTOR'])
            providers = ul.select(self.SEARCH_CONFIG['PROVIDER_SELECTOR'])
            dates = ul.select(self.SEARCH_CONFIG['MODIFIED_DATE_SELECTOR'])
            links = ul.select(self.SEARCH_CONFIG['ITEM_LINK_SELECTOR'])

            if len(titles) == len(providers) == len(dates) == len(links):
                self.log.info("Succeed to get info list")
                for title, provider, date, link in zip(titles, providers, dates, links):
                    result.append({
                        'title': title.get_text().strip(),
                        'provider': provider.get_text().strip(),
                        'date': date.get_text().strip(),
                        'link': link.attrs['href']
                    })
                    self.log.info(result[-1]) 
            else:
                raise Exception("title, provider, date length is not equal")
        else:
            raise Exception(f"HTTP error: {response.status_code}")
        
        return result

    
if __name__ == "__main__":
    search = DataPortalSearcher()
    result = search.get_info_lists(config['SEARCH_CONFIG']['SEARCH_KEYWORD'][0])
    print(len(result))
    result = search.get_info_lists(config['SEARCH_CONFIG']['SEARCH_KEYWORD'][1])
    print(len(result))