from util.logger import logger
from util.conf import config
import abc

class IDataPortalSearcher:
    """
    공공데이터 포털 검색 인터페이스를 제공
    """
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def get_info(self, keyword:str):
        pass

class DataPortalSearcher(IDataPortalSearcher): 
    """
    공공데이터 포털 검색 구현체
    """
    def __init__(self) -> None:
        super().__init__()
        self.log = logger.get_logger(__name__)
        return
    
    def get_info(self, keyword: str):
        self.log.info(f"Start to search by keyword: {keyword}")
        return
    
if __name__ == "__main__":
    search = DataPortalSearcher()
    search.get_info(config['search_keyword'][0])
    search.get_info(config['search_keyword'][1])