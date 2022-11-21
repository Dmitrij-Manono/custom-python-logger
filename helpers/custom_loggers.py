import coloredlogs
import logging
import os
import time
import inspect
import traceback
import sys

######################################## Custom Console Logger ########################################
STREAM_DEFAULT_LOG_LEVEL = logging.DEBUG
STREAM_DEFAULT_LOG_NAME = "cli_Log"
#DEFAULT FIELD STYLES
STREAM_DEFAULT_FIELD_STYLES = {'lineno': {'color': 'cyan'}, 'name': {'color': 'black'}, 'levelname': {'color': 'black', 'bold': True, 'bright': True},'funcName': {'color': 'black'}, 'asctime': {'color': 'green'}, 'message': {'color': 'white'}, 'filename': {'color': 'black'},'module': {'color': 'blue'}, 'relativeCreated': {'color': 'green'}, 'msecs': {'color': 'green'}}
# FIELD STYLES FOR ALERT LEVEL
STREAM_ALERT_FIELD_STYLES = {'lineno': {'color': 'red'}, 'name': {'color': 'black'}, 'levelname': {'color': 'black', 'bold': True, 'bright': True},'funcName': {'color': 'black'}, 'asctime': {'color': 'green'}, 'message': {'color': 'white'}, 'filename': {'color': 'black'},'module': {'color': 'blue'}, 'relativeCreated': {'color': 'green'}, 'msecs': {'color': 'green'}}

# DEFAULT LEVEL STYLES
STREAM_DEFAULT_LEVEL_STYLES = {'info': {'color': 40, 'bold': True}, 'warning': {'color': 'yellow', 'bold': True}, 'error': {'color': 196, 'bold': True}, 'debug': {'color': 51,'bald': True}, 'critical': {'color': 'white', 'bold': True, 'background': 'red'},'exception': {'color': 'cyan', 'bold': True}, 'alert': {'color': 166, 'bold': True}}
# DEFAULT COMSOLE LOG FORMAT
STREAM_LOG_DEFAULT_FORMAT = '|%(asctime)s|%(name)s|%(levelname)s|   %(message)s   |%(filename)s|%(funcName)s|%(lineno)d|%(module)s|%(relativeCreated)d|%(msecs)d|'
# FORMAT FOR WARNING LEVEL
STREAM_LOG_WARNING_FORMAT = '|%(asctime)s|%(name)s|%(levelname)s|   %(message)s   | %(filename)s, %(funcName)s, %(lineno)d, %(module)s, %(relativeCreated)d, %(msecs)d|, %(message)s|'
# FORMAT FOR ALERT LEVEL
STREAM_LOG_ALERT_FORMAT = '|%(asctime)s|%(name)s|%(levelname)s|   %(message)s   |'
# FORMAT FOR IMPORTANT LEVEL
STREAM_LOG_IMPORTANT_FORMAT = '|%(asctime)s|%(name)s|%(levelname)s|   %(message)s   |'
# FORMAT FOR EXCEPTION LEVEL
STREAM_LOG_EXCEPTION_FORMAT = '|%(asctime)s|%(name)s|%(levelname)s|   %(message)s   |'
# FORMAT FOR ERROR LEVEL
STREAM_LOG_ERROR_FORMAT = '|%(asctime)s|%(name)s|%(levelname)s|   %(message)s   |, %(lineno)d, %(lineno)d'
STREAM_DEFAULT_TIME_FORMAT = '%H:%M:%S.%f'

######################################## Custom File Logger ########################################

DEFAULT_LOG_DIR = "logs"

FILE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
FILE_LOG_DEFAULT_FORMAT = '%(asctime)s|%(levelname)s|   %(message)s   |%(name)s %(filename)s:%(funcName)s:%(lineno)d, %(process)d, %(thread)d, %(threadName)s, %(processName)s|'


# Class ConsoleLogger returns a logger for class calling it, logger is logging only to console, with different styles
# class ConsoleLogger has custom methods for logging at different levels
# inspect.stack() will be used to get correct caller name, line number, file name, function name etc

class ConsoleLogger():
    def __init__(self, log_level=STREAM_DEFAULT_LOG_LEVEL, log_name=STREAM_DEFAULT_LOG_NAME, field_styles=STREAM_DEFAULT_FIELD_STYLES, level_styles=STREAM_DEFAULT_LEVEL_STYLES, log_format=STREAM_LOG_DEFAULT_FORMAT, time_format=STREAM_DEFAULT_TIME_FORMAT):
        self.log_level = log_level
        self.log_name = log_name
        self.field_styles = field_styles
        self.level_styles = level_styles
        self.log_format = log_format
        self.time_format = time_format
        self.logger = logging.getLogger(self.log_name)
        # add alert level
        logging.addLevelName(100, "ALERT")
        logging.addLevelName(200, "IMPORTANT")
        logging.addLevelName(300, "EXCEPTION")
        self.logger.setLevel(self.log_level)
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(self.log_level)
        self.stream_formatter = coloredlogs.ColoredFormatter(fmt=self.log_format, field_styles=self.field_styles, level_styles=self.level_styles, datefmt=self.time_format)
        self.stream_handler.setFormatter(self.stream_formatter)
        self.logger.addHandler(self.stream_handler)
        self.logger.propagate = False


    # creates new record for logger with file name, function name, line number, message, level etc
    # addes exception type error to record if exception is passed
    def create_record(self, msg, level, exception=None):
        stack = inspect.stack()
        record = logging.LogRecord(name=self.log_name, level=level, pathname=stack[2][1], lineno=stack[2][2], msg=msg, args=None, exc_info=exception, func=stack[2][3])
        return record



    def info(self, msg, *args, **kwargs):
        record = self.create_record(msg, logging.INFO)
        self.logger.handle(record)

    def warning(self, msg, *args, **kwargs):
        record = self.create_record(msg, logging.WARNING)
        self.logger.handle(record)
    
    def error(self, msg, *args, **kwargs):
        record = self.create_record(msg, logging.ERROR)
        self.logger.handle(record)

    def debug(self, msg, *args, **kwargs):
        record = self.create_record(msg, logging.DEBUG)
        self.logger.handle(record)

    def critical(self, msg, *args, **kwargs):
        record = self.create_record(msg, logging.CRITICAL)
        self.logger.handle(record)

    def alert(self, msg, *args, **kwargs):
        record = self.create_record(level=100, msg=msg)
        self.logger.handle(record)

    def important(self, msg, *args, **kwargs):
        record = self.create_record(level=200, msg=msg)
        self.logger.handle(record)
    
    # exception level is used for logging exceptions
    # prints exception type, exception message
    def exception(self, msg, *args, **kwargs):
        record = self.create_record(level=300, msg=msg, exception=sys.exc_info())
        self.logger.handle(record)
    

    





def main():
    logger = ConsoleLogger()
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.alert("This is an alert message")
    logger.important("This is an important message")
    logger.error("This is an error message")
    logger.debug("This is a debug message")
    logger.critical("This is a critical message")
    #print(logger.find_caller())
    try :
        1/0
    except Exception as e:
        logger.exception(f"This is an exception message \'{e}\'") 
        

if __name__ == "__main__":
    main()


