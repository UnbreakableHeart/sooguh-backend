from util.logger import logger
import abc

class IDataParseStrategy:
    """
    """
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def parse(self, file):
        pass

class ExcelParser(IDataParseStrategy):
    """
    """
    def __init__(self) -> None:
        super().__init__()
        return
    
    def parse(self, file):
        return 

class ClothingBinDataParser:
    """
    """
    def __init__(self) -> None:
        self.parse_strategy: IDataParseStrategy = None
        pass

    def set_strategy(self, parse_strategy:IDataParseStrategy):
        self.parse_strategy = parse_strategy
        return 

    def parse(self, file):
        return self.parse_strategy.parse(file)


