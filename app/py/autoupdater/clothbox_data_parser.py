"""A module for parsing address from a file.

This module defines the interface and the implementation of the class that parses address from a file.

Example:
    >>> parser = ClothBoxDataParser()
    >>> parser.set_strategy(CsvParser())
    >>> result = parser.parse('res/data.csv')
    >>> print(result)
"""

import sys
import os
sys.path.append(os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ))
from autoupdater.util import logger
from autoupdater.util.conf import config
import abc
import os
from typing import List
import pandas as pd
from overrides import overrides

log = logger.get_logger(__name__)

class IDataParseStrategy:
    """An abstract base class for data parse strategies.

    This interface defines the methods that should be implemented by a class that parses
    """
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def parse_address(self, file_path:str) -> List[str]:
        """ A method to parse the address from the file.

        Args:
            file (str): The file to parse.

        Returns:
            List[str]: A list of addresses.
        """
        pass

class CsvParser(IDataParseStrategy):
    """ A class that parses address from a csv file.
    """
    def __init__(self) -> None:
        super().__init__()
        return
    
    @overrides
    def parse_address(self, file_path:str, index_words: List[str] = None) -> List[str]:
        log.info(f'Parsing data from {file_path}')
        try:
            df = pd.read_csv(file_path, encoding='cp949', on_bad_lines='skip')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(file_path, encoding='euc-kr', on_bad_lines='skip')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')

        header = df.columns.tolist()

        column_index = None

        for word in index_words:
            for i in range(len(header)):
                if word in header[i]:
                    column_index = i
                    break
            if column_index is not None:
                break

        if column_index is None:
            log.error(f'Cannot find the index column in the file: {file_path}')
            return None
        
        values = df.iloc[:, column_index].values.tolist()
        values = [value for value in values if not pd.isna(value)]
        return values

class ClothBoxDataParser:
    """ A class that parses address from a file using a strategy pattern.
    """
    def __init__(self) -> None:
        self.parse_strategy: IDataParseStrategy = None
        pass

    def set_strategy(self, parse_strategy:IDataParseStrategy):
        """Set the parse strategy.

        Args:
            parse_strategy (IDataParseStrategy): The parse strategy to set.
        """
        self.parse_strategy = parse_strategy
        return 

    def parse_address(self, file) -> List[str]:
        """ Parse the address from the file.

        Args:
            file (str): The file to parse.

        Returns:
            List[str]: A list of addresses.
        """
        return self.parse_strategy.parse_address(file, config['ADDRESS_PARSING_WORDS'])
    
if __name__ == '__main__':
    parser = ClothBoxDataParser()
    parser.set_strategy(CsvParser())
    excel_files = [os.path.join('res', file) for file in os.listdir('res') if file.endswith('.csv')]
    for excel_file in excel_files:
        result = parser.parse_address(excel_file)
        log.info(result)