import sys
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
from autoupdater.clothbox_manager import IClothBoxManager, ClothBoxManager
from autoupdater.data_portal_searcher import IDataPortalSearcher, DataPortalSearcher
from autoupdater.data_download_driver import DataDownloadDriver
from autoupdater.util.conf import config
from autoupdater.util import logger
from typing import List
import traceback

log = logger.get_logger(__name__)

class ClothBoxUpdater:
    '''This class is used to update the cloth box data.

    Attributes:
        clothbox_db (IClothBoxManager): The db manager for cloth box data.
        data_portal_searcher (IDataPortalSearcher): The data portal searcher.
        data_download_driver (DataDownloadDriver): The driver for downloading data.
    '''
    clothbox_db: IClothBoxManager = None
    data_portal_searcher: IDataPortalSearcher = None
    data_download_driver: DataDownloadDriver = None

    def __init__(self, clothbox_db: IClothBoxManager, data_portal_searcher: IDataPortalSearcher) -> None:
        self.clothbox_db = clothbox_db
        self.data_portal_searcher = data_portal_searcher
        self.data_download_driver = DataDownloadDriver()
        pass

    def start_update(self) -> None:
        """Start to udpate cloth box data.
        """
        log.info("Start to udpate cloth box")
        search_data_list = self._search_data()
        if search_data_list is None:
            log.error("No data found.")
            return
        for search_data in search_data_list:
            try:
                self.data_download_driver.open_url(config['DATA_PORTAL_URL']+search_data['link'])
                self.data_download_driver.download_data(config['DOWNLOAD_BUTTON_XPATH'])
            except Exception as e:
                log.error(f"Failed to download data: {search_data['title']}")
                log.error(f"Error: {e}")
                log.error(traceback.format_exc())
                continue
        return

    def _search_data(self) -> List:
        last_update_date = self.clothbox_db.read_last_update_date()
        search_data_list = []
        if last_update_date is None:
            log.info("No last update date found. Start to search all data.")
            for keyword in config['SEARCH_CONFIG']['SEARCH_KEYWORD']:
                search_data_list.extend(self.data_portal_searcher.search_data(keyword))
        else:
            log.info(f"Last update date found: {last_update_date}")
            for keyword in config['SEARCH_CONFIG']['SEARCH_KEYWORD']:
                search_data_list.extend(self.data_portal_searcher.search_data(keyword, last_update_date.strftime('%Y-%m-%d')))
        return search_data_list

if __name__ == "__main__":
    updater = ClothBoxUpdater(ClothBoxManager(), DataPortalSearcher())
    updater.start_update()