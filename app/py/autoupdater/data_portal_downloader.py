from util.logger import logger
import abc

class IDataPortalDownloader:
    """
    공공데이터 포털의 데이터 다운로드 인터페이스를 제공
    """
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def download_data(self, url:str):
        pass

class DataPortalDownloader(IDataPortalDownloader): 
    """
    공공데이터 포털의 데이터 다운로드 구현체
    """
    def __init__(self) -> None:
        super().__init__()
        self.log = logger.get_logger(__name__)
        return
    
    def download_data(self, url:str):
        self.log.info(f"Start to download on url: {url}")
        return
    
if __name__ == "__main__":
    downloader = DataPortalDownloader()
    downloader.download_data('www.naver.com')
    