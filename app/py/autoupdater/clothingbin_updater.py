from util.logger import logger

class ClothingBinUpdater:
    '''
    의류 수거함 데이터를 업데이트하는 기능을 제공
    '''
    def __init__(self) -> None:
        self.log = logger.get_logger(__name__)
        pass

    def start_update(self) -> None:
        """
        공공 데이터포털에서 제공하는 의류 수거함 데이터를 DB에 업데이트
        """
        self.log.info("Start to udpate clothing bin")
        return

if __name__ == "__main__":
    updater = ClothingBinUpdater()
    updater.start_update()