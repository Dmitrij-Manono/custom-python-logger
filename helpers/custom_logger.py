import coloredlogs
import logging
import os
import time
import inspect
#import traceback
import sys
import datetime


######################################## Custom Console Logger ########################################
STREAM_DEFAULT_LOG_LEVEL = logging.DEBUG
STREAM_DEFAULT_LOG_NAME = "cli_Log"
#DEFAULT FIELD STYLES
STREAM_DEFAULT_FIELD_STYLES = {'lineno': {'color': 127}, 'name': {'color': 'black'}, 'levelname': {'color': 180, 'bold': True},'funcName': {'color': 'black'}, 'asctime': {'color': 'black', 'bold': True}, 'message': {'color': 'white'}, 'filename': {'color': 'black'},'module': {'color': 'black'}, 'relativeCreated': {'color': 'green'}, 'msecs': {'color': 'green'}}
# FIELD STYLES FOR ALERT LEVEL
STREAM_ALERT_FIELD_STYLES = {'lineno': {'color': 'red'}, 'name': {'color': 'black'}, 'levelname': {'color': 'black', 'bold': True, 'bright': True},'funcName': {'color': 'black'}, 'asctime': {'color': 'green'}, 'message': {'color': 'white'}, 'filename': {'color': 'black'},'module': {'color': 'blue'}, 'relativeCreated': {'color': 'green'}, 'msecs': {'color': 'green'}}

# DEFAULT LEVEL STYLES
STREAM_DEFAULT_LEVEL_STYLES = {'info': {'color': 'green', 'bold': False}, 'warning': {'color': 'yellow', 'bold': True}, 'error': {'color': 196, 'bold': False}, 'debug': {'color': 27,'bald': True}, 'critical': {'color': 'white', 'bold': True, 'background': 'red'},'exception': {'color': 196, 'bold': True}, 'alert': {'color': 166, 'bold': True}, 'important': {'color': 40, 'bold': True}, 'input_required': {'color': 213, 'bold': True}, 'message': {'bold': True}}
# DEFAULT COMSOLE LOG FORMAT
STREAM_LOG_DEFAULT_FORMAT = '|%(asctime)s|%(levelname)s|   %(message)s   |%(filename)s|%(funcName)s|%(lineno)d|%(name)s|' #%(module)s|
# FORMAT FOR ALERT LEVEL
STREAM_LOG_LESSINFO_FORMAT = '|%(asctime)s|%(levelname)s|   %(message)s'

STREAM_DEFAULT_TIME_FORMAT = '%H:%M:%S.%f'

######################################## Custom File Logger ########################################

DEFAULT_FILE_LOG_DIR = "logs"
DEFAULT_FILE_LOG_NAME = "app_Log"
DEFAULT_FILE_LOG_LEVEL = logging.DEBUG
DEFAULT_FILE_LOG_FORMAT = '%(asctime)s|%(levelname)s|   %(message)s    |%(filename)s|%(funcName)s|%(lineno)d|%(name)s|' #%(module)s|

DEFAULT_FILE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'



# Class ConsoleLogger returns a logger for class calling it, logger is logging only to console, with different styles
# class ConsoleLogger has custom methods for logging at different levels
# inspect.stack() will be used to get correct caller name, line number, file name, function name etc

class CustomLogger():
    def __init__(self, log_level=STREAM_DEFAULT_LOG_LEVEL, log_name=STREAM_DEFAULT_LOG_NAME, field_styles=STREAM_DEFAULT_FIELD_STYLES, level_styles=STREAM_DEFAULT_LEVEL_STYLES, log_format=STREAM_LOG_DEFAULT_FORMAT, time_format=STREAM_DEFAULT_TIME_FORMAT):
        self.log_level = log_level
        self.log_name = log_name
        self.field_styles = field_styles
        self.level_styles = level_styles
        self.log_format = log_format
        self.time_format = time_format
        self.logger = logging.getLogger(self.log_name)
        logging.addLevelName(35, "ALERT")
        logging.addLevelName(25, "IMPORTANT")
        logging.addLevelName(45, "EXCEPTION")
        logging.addLevelName(200, "MESSAGE")
        logging.addLevelName(300, "INPUT_REQUIRED")
        self.logger.setLevel(self.log_level)
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(self.log_level)
        self.stream_formatter = coloredlogs.ColoredFormatter(fmt=self.log_format, field_styles=self.field_styles, level_styles=self.level_styles, datefmt=self.time_format)
        self.stream_handler.setFormatter(self.stream_formatter)
        self.logger.addHandler(self.stream_handler)
        self.logger.propagate = False
        # file handler variables
        self.file_handler = None
        self.file_formatter = None
        self.file_log_dir = None
        self.file_log_name = None
        self.file_log_level = None
        self.file_log_format = None
        self.file_time_format = None


    # create_file_handler method creates a file handler for logger and adds it to logger
    # checks if file handler already exists, if yes, removes it and creates a new one
    # checks if directory or file exists, if not, creates them, adds date to file name

    def create_file_handler(self, log_dir=DEFAULT_FILE_LOG_DIR, log_name=DEFAULT_FILE_LOG_NAME, log_level=DEFAULT_FILE_LOG_LEVEL, log_format=DEFAULT_FILE_LOG_FORMAT, time_format=DEFAULT_FILE_TIME_FORMAT):
        self.file_log_dir = log_dir
        self.file_log_name = log_name
        self.file_log_level = log_level
        self.file_log_format = log_format
        self.file_time_format = time_format
        if self.file_handler:
            self.logger.removeHandler(self.file_handler)
        if not os.path.exists(self.file_log_dir):
            os.makedirs(self.file_log_dir)
        self.file_handler = logging.FileHandler(os.path.join(self.file_log_dir, self.file_log_name + "_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".log"))
        self.file_handler.setLevel(self.file_log_level)
        self.file_formatter = logging.Formatter(fmt=self.file_log_format, datefmt=self.file_time_format)
        self.file_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(self.file_handler)

    


    # set colored formatter to default format
    def set_default_formatter(self):
        self.stream_formatter = coloredlogs.ColoredFormatter(fmt=STREAM_LOG_DEFAULT_FORMAT, field_styles=self.field_styles, level_styles=self.level_styles, datefmt=self.time_format)
        self.stream_handler.setFormatter(self.stream_formatter)
    # set new format for colored formatter for specific level
    def set_colored_formatter_format(self, log_format):
        self.log_format = log_format
        self.stream_formatter = coloredlogs.ColoredFormatter(fmt=self.log_format, field_styles=self.field_styles, level_styles=self.level_styles, datefmt=self.time_format)
        self.stream_handler.setFormatter(self.stream_formatter)

    
    # set new formatter for specific level
    def set_formatter(self, level, log_format, time_format):
        self.log_format = log_format
        self.time_format = time_format
        self.stream_formatter = logging.Formatter(fmt=self.log_format, datefmt=self.time_format)
        self.stream_handler.setFormatter(self.stream_formatter)
        self.logger.setLevel(level)
        self.stream_handler.setLevel(level)
    
    
    # set new log level
    def set_level(self, level):
        self.logger.setLevel(level)
        self.stream_handler.setLevel(level)
    
    # set new log name
    def set_name(self, name):
        self.log_name = name
        self.logger = logging.getLogger(self.log_name)
    
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

    def important(self, msg, *args, **kwargs):
        record = self.create_record(level=25, msg=msg)
        self.set_colored_formatter_format(STREAM_LOG_LESSINFO_FORMAT)
        self.logger.handle(record)
        self.set_default_formatter()
    
    # exception level is used for logging exceptions
    # prints exception type, exception message
    def exception(self, msg, *args, **kwargs):
        record = self.create_record(level=45, msg=msg, exception=sys.exc_info())
        self.logger.handle(record)
    
    # alert level is used for logging alerts with different style format
    def alert(self, msg, *args, **kwargs):
        record = self.create_record(level=35, msg=msg)
        # change output format for alert level
        self.set_colored_formatter_format(STREAM_LOG_LESSINFO_FORMAT)
        self.logger.handle(record)
        # change output format back to default
        self.set_default_formatter()
    
    def input_required(self, msg, *args, **kwargs):
        record = self.create_record(level=300, msg=msg)
        self.set_colored_formatter_format(STREAM_LOG_LESSINFO_FORMAT)
        self.logger.handle(record)
        self.set_default_formatter()
    
    def message(self, msg, *args, **kwargs):
        record = self.create_record(level=200, msg=msg)
        self.set_colored_formatter_format(STREAM_LOG_LESSINFO_FORMAT)
        self.logger.handle(record)
        self.set_default_formatter()



def main():
    logger = CustomLogger()
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.alert("This is an alert message")
    logger.important("This is an important message")
    logger.error("This is an error message")
    logger.debug("This is a debug message")
    logger.critical("This is a critical message")
    logger.input_required("This is an input required message")
    logger.message("This is a message")
    #print(logger.find_caller())
    try :
        1/0
    except Exception as e:
        logger.exception(f"This is an exception message \'{e}\'") 
        

if __name__ == "__main__":
    main()


