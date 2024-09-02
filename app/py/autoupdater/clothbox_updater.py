import sys
import os
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
from autoupdater.clothbox_manager import IClothBoxManager, ClothBoxManager
from autoupdater.data_portal_searcher import IDataPortalSearcher, DataPortalSearcher
from autoupdater.data_download_driver import DataDownloadDriver
from autoupdater.clothbox_data_parser import ClothBoxDataParser, CsvParser
from autoupdater.util.conf import config
from autoupdater.util.logger import Logger
from dotenv import load_dotenv
from typing import List
import requests, json
import traceback
import re

log = Logger.get_instance(__name__)
load_dotenv()

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
        self.file_parser = ClothBoxDataParser()
        self.file_parser.set_strategy(CsvParser())
        pass

    def start_update(self) -> None:
        """Start to udpate cloth box data.
        """
        log.info("Start to udpate cloth box")
        search_data_list = self._search_data()
        print(search_data_list)
        if search_data_list is None or len(search_data_list) == 0:
            log.error("No data found.")
            return
        update_info = []
        for search_data in search_data_list:
            providing_name = search_data['provider']
            try:
                self.data_download_driver.open_url(config['DATA_PORTAL_URL']+search_data['link'])
                self.data_download_driver.download_data(config['DOWNLOAD_BUTTON_XPATH'])
                result = self._read_res_file()
                self.clothbox_db.delete_clothbox_data(providing_name)
                for data in result:
                    try:
                        address, coordinates = self._get_lat_lng(data)
                        print(address, providing_name, coordinates)
                        self.clothbox_db.write_clothbox_data(address, providing_name, [coordinates['lon'], coordinates['lat']])
                    except Exception as e:
                        log.error(f"Failed to write data: {data}")
                        log.error(f"Error: {e}")
            except Exception as e:
                log.error(f"Failed to write data: {search_data['title']}")
                log.error(f"Error: {e}")
                log.error(traceback.format_exc())
                continue
            update_info.append(providing_name)
        self.clothbox_db.write_update_info(update_info)
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
    
    def _read_res_file(self, directory='res') -> List:
        files = os.listdir(directory)
        data_list = []
        for file in files:
            log.info(f'Parsing data from {directory}/{file}')
            result = None
            try:
                result = self.file_parser.parse_address(f'{directory}/{file}')
            except Exception as e:
                log.error(f'Failed to parse data from {directory}/{file}')
                log.error(e)
                continue
            os.remove(f'{directory}/{file}')
            if result is None:
                log.error(f'Failed to parse data from {directory}/{file}')
                continue
            data_list.extend(result)
        return data_list
    
    def _get_lat_lng(self, address: str) -> tuple:
        address = re.sub(r'\s*\(.*?\)\s*', '', address)
        url = config['KAKAO_ADDRESS_API_URL'] + address
        kakao_api_key = os.getenv('KAKAO_API_KEY')

        headers = {'Authorization': kakao_api_key}
        api_json = json.loads(str(requests.get(url,headers=headers).text))

        address = api_json['documents'][0]['address']
        coordinates = {"lat": float(address['y']), "lon": float(address['x'])}
        return address['address_name'], coordinates
        
if __name__ == "__main__":
    updater = ClothBoxUpdater(ClothBoxManager(), DataPortalSearcher())
    updater.start_update()

    