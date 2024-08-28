import logging

class Logger:
    _instance = None

    def __new__(cls, name):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.__initialize(name)
        return cls._instance

    def __initialize(self, name):
        self.__logger = logging.getLogger(name)
        
        # 로그 포멧 정의
        formatter = logging.Formatter(
            '%(asctime)s:[%(name)s][%(levelname)s] - %(filename)s:%(lineno)d - %(message)s')
        # 스트림 핸들러 정의
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('Log.log', mode='a', encoding='utf-8')
        # 각 핸들러에 포멧 지정
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        # 로거 인스턴스에 핸들러 삽입
        self.__logger.addHandler(stream_handler)
        self.__logger.addHandler(file_handler)
        # 로그 레벨 정의
        self.__logger.setLevel(logging.DEBUG)

    @classmethod
    def get_instance(cls, name):
        if cls._instance is None:
            cls(name)
        return cls._instance.__logger