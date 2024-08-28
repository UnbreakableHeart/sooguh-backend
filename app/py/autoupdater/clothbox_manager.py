"""A module for managing the db.

This module defines the interface and the implementation of the class that manages the db.
The class is responsible for reading and writing data to the db.

Example:
    >>> manager = ClothBoxManager()
    >>> ret = manager.delete_clothbox_data("Seoul")
    >>> ret = manager.write_clothbox_data("Suwon", "수원", [37.5665, 126.9780])
    >>> ret = manager.write_update_info(["수원"])
    >>> ret = manager.read_last_update_date()
    >>> ret = manager.get_clothbox_data("Suwon")
"""

import sys
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
from autoupdater.util.logger import Logger
from autoupdater.util.conf import config
import abc
import pymongo
from datetime import datetime
from overrides import overrides
from typing import List
from dotenv import load_dotenv
import os
from pymongo.server_api import ServerApi

log = Logger.get_instance(__name__)

class IClothBoxManager(metaclass=abc.ABCMeta):
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
    def write_clothbox_data(self, address:str, providing_name:str, coordinates:List[float]) -> bool:
        """Abstract method to write the clothbox data to the db.

        Args:
            address (str): The address of the clothbox.
            providing_name (str): The name of the provider.
            coordinates (List[float]): The coordinates of the clothbox.

        Returns:
            bool: True if the clothbox data was written successfully, False otherwise.
        """
        pass

    @abc.abstractmethod
    def get_clothbox_data(self, providing_name:str) -> List[str]:
        """Abstract method to get the clothboxes from the db by a specific organization.

        Args:
            providing_name (str): The name of the provider.

        Returns:
            List[str]: A list of the address of clothboxes.
        """
        pass

    @abc.abstractmethod
    def delete_clothbox_data(self, address:str) -> bool:
        """Abstract method to delete the clothbox data from the db.

        Args:
            address (str): The address of the clothbox.

        Returns:
            bool: True if the clothbox data was deleted successfully, False otherwise.
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
    def write_clothbox_data(self, address:str, providing_name:str, coordinates:List[float]) -> bool:
        """Write the clothbox data to the db.

        Args:
            address (str): The address of the clothbox.
            providing_name (str): The name of the provider.
            coordinates (List[float]): The coordinates of the clothbox. The order should be [longitude, latitude].

        Returns:
            bool: True if the clothbox data was written successfully, False otherwise.
        """
        log.info("Writing the clothbox data to the db...")
        clothbox_collection = self.db[os.environ.get('DB_COLLECTION_CLOTH_BOX')]
        update_query = {
            "address": address,
            "providing_name": providing_name,
            "location": {
                "type": "Point",
                "coordinates": coordinates
            }
        }
        result = clothbox_collection.update_one({"address": address}, {"$set": update_query}, upsert=True)
        return result.acknowledged
    
    @overrides
    def get_clothbox_data(self, providing_name: str) -> List[str]:
        """Get the clothboxes from the db by a specific organization.

        Args:
            providing_name (str): The name of the provider.

        Returns:
            List[str]: A list of the address of clothboxes.
        """
        log.info(f"Getting the clothboxes provided by the organization: {providing_name}...")
        clothbox_collection = self.db[os.environ.get('DB_COLLECTION_CLOTH_BOX')]
        docs = list(clothbox_collection.find({
            "providing_name": providing_name
        }))
        return [doc["address"] for doc in docs]
    
    @overrides
    def delete_clothbox_data(self, address:str) -> bool:
        """Delete the clothbox data from the db.

        Args:
            address (str): The address of the clothbox.

        Returns:
            bool: True if the clothbox data was deleted successfully, False otherwise.
        """
        log.info(f"Deleting the clothbox data from the db...: {address}")
        clothbox_collection = self.db[os.environ.get('DB_COLLECTION_CLOTH_BOX')]
        result = clothbox_collection.delete_one({"address": address})
        return result.acknowledged
    
if __name__ == "__main__":
    manager = ClothBoxManager()
    print(manager.delete_clothbox_data("Seoul"))
    print(manager.delete_clothbox_data("Incheon"))
    print(manager.write_clothbox_data("송파동 18-3", "송파구", [127.10801000757587,	37.506659051679726]))
    print(manager.write_clothbox_data("송파동 22-6", "송파구", [127.109457691,	37.510190298]))
    print(manager.write_clothbox_data("송파동 21-11", "송파구", [127.106755185,	37.507608279]))
    print(manager.write_update_info(["송파구"]))
    print(manager.read_last_update_date())
    print(manager.get_clothbox_data("송파구"))
