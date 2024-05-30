

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

class IDataPortalSearcher:
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def get_info_lists(self, keyword:str):
        pass

class DataPortalSearcher(IDataPortalSearcher): 
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
    def get_info_lists(self, keyword: str):
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
    
    def _get_info_list(self, url: str):
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