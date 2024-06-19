import sys
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
from autoupdater.util import logger
from autoupdater.util.conf import config
import abc
import pymongo
from datetime import datetime
from overrides import overrides
from typing import List
from dotenv import load_dotenv
import os
from pymongo.server_api import ServerApi

log = logger.get_logger(__name__)

class IClothBoxManager:
    """An abstract base class for db manager.

    This interface defines the methods that should be implemented by a class that manages the db.
    """
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def read_last_update_date(self) -> datetime:
        """Abstract method to read the last update date from the db.

        Returns:
            datetime: The last update date.
        """
        pass

    @abc.abstractmethod
    def write_update_info(self, updated_items:List[str]) -> bool:
        """Abstract method to write the update info to the db.

        Args:
            updated_items (List[str]): A list of items that were updated.

        Returns:
            bool: True if the update info was written successfully, False otherwise.
        """
        pass

    @abc.abstractmethod
    def write_clothbox_data(self, address:str) -> bool:
        """Abstract method to write the clothbox data to the db.

        Args:
            address (str): The address of the clothbox.

        Returns:
            bool: True if the clothbox data was written successfully, False otherwise.
        """
        pass

class ClothBoxManager(IClothBoxManager): 
    """A class for managing the db.

    Attributes:
        db (pymongo.database.Database): The database object.
    """
    def __init__(self) -> None:
        super().__init__()
        log.info("Connecting to the db...")
        load_dotenv()
        db_uri = os.environ.get('DB_URI')
        client = pymongo.MongoClient(db_uri, server_api=ServerApi('1'))

        try:
            client.admin.command('ping')
            log.info("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            log.error("Unable to connect to the database.")
            log.error(e)

        self.db = client[os.environ.get('DB_NAME')]
        return
    
    @overrides
    def read_last_update_date(self) -> datetime:
        """Read the last update date from the db.

        Returns:
            datetime: The last update date.
        """
        log.info("Reading the last update date from the db...")
        update_info_collection = self.db[os.environ.get('DB_COLLECTION_UPDATE_INFO')]
        doc = list(update_info_collection.find({
            "update_date": {"$exists": True}
        }).sort("update_date", -1).limit(1))
        
        if len(doc) == 0:
            log.info("No update info found.")
            return None
        return doc[0]["update_date"]

    
    @overrides
    def write_update_info(self, updated_items:List[str]) -> bool:
        """ Write the update info to the db.

        Args:
            updated_items (List[str]): A list of items that were updated.

        Returns:
            bool: True if the update info was written successfully, False otherwise.
        """
        log.info("Writing the update info to the db...")
        update_date = datetime.now()
        update_info_collection = self.db[os.environ.get('DB_COLLECTION_UPDATE_INFO')]
        update_query = {
                "update_date": update_date,
                "updated_items": updated_items
        }
        result = update_info_collection.update_one({"update_date": update_date}, {"$set": update_query}, upsert=True)
        return result.acknowledged

    @overrides
    def write_clothbox_data(self, address:str) -> bool:
        """Write the clothbox data to the db.

        Args:
            address (str): The address of the clothbox.

        Returns:
            bool: True if the clothbox data was written successfully, False otherwise.
        """
        log.info("Writing the clothbox data to the db...")
        clothbox_collection = self.db[os.environ.get('DB_COLLECTION_CLOTH_BOX')]
        update_query = {
            "address": address,
            "location": {
                "type": "Point",
                "coordinates": self._get_coordinates(address)
            }
        }
        result = clothbox_collection.update_one({"address": address}, {"$set": update_query}, upsert=True)
        return result.acknowledged

    def _get_coordinates(self, address:str) -> List[float]:
        log.info("Getting the coordinates of the address...")
        # TODO: Implement the logic to get the coordinates of the address.
        return [0.0, 0.0]
    
if __name__ == "__main__":
    manager = ClothBoxManager()
    manager.write_clothbox_data("Seoul")
    manager.write_update_info(["Seoul"])
    print(manager.read_last_update_date())