from util.logger import logger
import abc

class IClothBoxManager:
    """
    TODO
    """
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def read_date_section(self, section:str):
        pass

    @abc.abstractmethod
    def write_clothbox_data(self):
        pass

class ClothBoxManager(IClothBoxManager): 
    """
    TODO
    """
    def __init__(self) -> None:
        super().__init__()
        self.log = logger.get_logger(__name__)
        return
    
    def read_date_section(self, section:str):
        return

    def write_clothbox_data(self):
        return
    
if __name__ == "__main__":
    manager = ClothBoxManager()
    manager.read_date_section("서울")
    manager.write_clothbox_data()