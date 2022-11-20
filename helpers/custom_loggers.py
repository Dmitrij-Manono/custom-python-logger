import coloredlogs
import logging
import os
import time

#SREAM_LOG_DEFAULT_STYLES = {'lineno': {'color': 'magenta'}, 'name': {'color': 'blue'}, 'levelname': {'color': 8},
# 'funcName': {'color': 'cyan'}, 'asctime': {'color': 'green'}, 'message': {'color': 'white'}, 'filename': {'color': 'yellow'}, 
# 'module': {'color': 'blue'}, 'process': {'color': 'magenta'}, 'thread': {'color': 'magenta'}, 'threadName': {'color': 'magenta'}, 
# 'created': {'color': 'green'}, 'relativeCreated': {'color': 'green'}, 'msecs': {'color': 'green'}, 'levelname': {'color': 'white', 'bold': True}, 
# 'levelno': {'color': 'white', 'bold': True}, 'exc_text': {'color': 'red'}, 'exc_info': {'color': 'red'}, 'stack_info': {'color': 'red'}}

STREAM_WARNING_STYLES = {'levelname': {'color': 'yellow', 'bold': True}, 'levelno': {'color': 'yellow', 'bold': True}, 'exc_text': {'color': 'red'}, 'exc_info': {'color': 'red'}, 'stack_info': {'color': 'red'}}
STREAM_DEFAULT_LEVEL_STYLES = {'info': {'color': 'green', 'bold': True}, 'warning': {'color': 'yellow', 'bold': True}, 
'error': {'color': 'red', 'bold': True}, 'debug': {'color': 'blue'}, 'critical': {'color': 'white', 'bold': True, 'background': 'red'}, 
'exception': {'color': 'red', 'bold': True, 'background': 'magenta'}, 'level 1337': {'color': 'magenta', 'bold': True}}

SREAM_LOG_DEFAULT_FORMAT = '%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d %(funcName)s %(message)s, %(exc_info)s, %(stack_info)s, %(threadName)s, %(thread)d, %(process)d, %(processName)s, %(created)f, %(relativeCreated)d, %(msecs)d'

class CustomFileLogger:
    def __init__(self, name='App_Logg', log_dir='logs', level=logging.DEBUG):
        self.name = name
        self.log_dir = log_dir
        self.level = level
        self.logger = self.get_logger()

    def get_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        log_file = os.path.join(self.log_dir, f"{self.name}_{time.strftime('_%Y-%m-%d')}.log")
        fh = logging.FileHandler(log_file)
        fh.setLevel(self.level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def info(self, msg):
        self.logger
    
    def warning(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def debug(self, msg):
        self.logger.debug(msg)
    
    def critical(self, msg):
        self.logger.critical(msg)
    
    def exception(self, msg):
        self.logger.exception(msg)
    
    def log(self, level, msg):
        self.logger.log(level, msg)
    
    def set_level(self, level):
        self.level = level
        self.logger.setLevel(level)

    
    def get_level(self):
        return self.level
    


    


class CustomStreamLogger:
    def __init__(self, name, level=logging.DEBUG):
        self.name = name
        self.level = level
        self.logger = self.get_logger()

    def get_logger(self):
        logger = logging.getLogger(self.name)
        #coloredlogs.DEFAULT_FIELD_STYLES = SREAM_LOG_DEFAULT_STYLES
        coloredlogs.DEFAULT_LEVEL_STYLES = STREAM_DEFAULT_LEVEL_STYLES
        coloredlogs.DEFAULT_LOG_FORMAT = SREAM_LOG_DEFAULT_FORMAT
        coloredlogs.install(level=self.level, logger=logger)
        return logger
    
    def info(self, msg):
        self.logger.info(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def debug(self, msg):
        self.logger.debug(msg)
    
    def critical(self, msg):
        self.logger.critical(msg)
    
    def exception(self, msg):
        self.logger.exception(msg)
    
    def log(self, level, msg):
        self.logger.log(level, msg)
    
    def set_level(self, level):
        self.level = level
        self.logger.setLevel(level)
    
    def alert(self, msg):
        self.logger.log(level=1337, msg=msg)
    
    def get_level(self):
        return self.level
    



    



def main():
    file_logger = CustomFileLogger("file_logger", "logs")
    stream_logger = CustomStreamLogger("stream_logger")


    stream_logger.info("This is a stream logger")
    stream_logger.alert("This is a stream TEST")
    stream_logger.warning("This is a stream logger")
    stream_logger.error("This is a stream logger")
    stream_logger.debug("This is a stream logger")
    stream_logger.critical("This is a stream logger")

    try:
        raise Exception("This is a stream logger")
    except Exception as e:
        stream_logger.exception(e)

       


if __name__ == "__main__":
    main()