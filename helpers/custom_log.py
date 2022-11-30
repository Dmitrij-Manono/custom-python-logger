import coloredlogs
import logging
import inspect
import sys
import traceback
import os
import datetime

######################################## Custom Console Logger ########################################
STREAM_DEFAULT_LOG_LEVEL = logging.DEBUG
STREAM_DEFAULT_LOG_NAME = "cli_Log"
#DEFAULT FIELD STYLES
STREAM_DEFAULT_FIELD_STYLES = {'lineno': {'color': 127}, 'name': {'color': 'black'}, 'levelname': {'color': 180, 'bold': True},'funcName': {'color': 'black'}, 'asctime': {'color': 'black', 'bold': True}, 'message': {'color': 'white'}, 'filename': {'color': 'black'},'module': {'color': 'black'}, 'relativeCreated': {'color': 'green'}, 'msecs': {'color': 'green'}}

# DEFAULT LEVEL STYLES
STREAM_DEFAULT_LEVEL_STYLES = {'info': {'color': 'green', 'bold': False}, 'warning': {'color': 'yellow', 'bold': True}, 'error': {'color': 196, 'bold': False}, 'debug': {'color': 27,'bald': True}, 'critical': {'color': 'white', 'bold': True, 'background': 'red'},'exception': {'color': 196, 'bold': True}, 'alert': {'color': 202, 'bold': True}, 'important': {'color': 40, 'bold': True}, 'user_input': {'color': 200, 'bold': True}, 'message': {'bold': True}, 'action_required': {'color': 129, 'bold': True}}
# DEFAULT COMSOLE LOG FORMAT
STREAM_LOG_DEFAULT_FORMAT = '|%(asctime)s|%(levelname)s|   %(message)s   |%(filename)s|%(funcName)s|%(lineno)d|%(name)s|' #%(module)s|
# FORMAT FOR ALERT LEVEL
STREAM_LOG_LESSINFO_FORMAT = '|%(asctime)s|%(levelname)s|   %(message)s'

STREAM_DEFAULT_TIME_FORMAT = '%H:%M:%S.%f'

######################################## Custom File Logger ########################################

DEFAULT_FILE_LOG_DIR = "logs"
DEFAULT_FILE_LOG_NAME = "app"
DEFAULT_FILE_LOG_LEVEL = logging.DEBUG
DEFAULT_FILE_LOG_FORMAT = '%(asctime)s|%(levelname)s|   %(message)s    |%(filename)s|%(funcName)s|%(lineno)d|%(name)s|' #%(module)s|
DEFAULT_FILE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# DEBUG = 10
USER_INPUT_LEVEL_NUM = 15
# INFO = 20
ALERT_LEVEL_NUM = 25
# WARNING = 30
IMPORTANT_LEVEL_NUM = 35
# ERROR = 40
EXCEPTION_LEVEL_NUM = 45
# CRITICAL = 50
ACTION_REQUIRED_LEVEL_NUM = 150
MESSAGE_LEVEL_NUM = 200


# Custom Log Class, which will be used to create custom loggers, which can be used in the other modules
# Has custom log levels, custom log levels can be added as per the requirement
class CustomLog(logging.Logger):
    def __init__(self, name=STREAM_DEFAULT_LOG_NAME, level=STREAM_DEFAULT_LOG_LEVEL, log_format=STREAM_LOG_DEFAULT_FORMAT, time_format=STREAM_DEFAULT_TIME_FORMAT, field_styles=STREAM_DEFAULT_FIELD_STYLES, level_styles=STREAM_DEFAULT_LEVEL_STYLES):
        super().__init__(name, level)
        self.log_name = name
        self.add_custom_log_levels()
        self.log_format = log_format
        self.time_format = time_format
        self.field_styles = field_styles
        self.level_styles = level_styles
        
        # add file handler and console handler
        self.add_file_handler(file_name=DEFAULT_FILE_LOG_NAME)
        self.add_console_handler()
        # add custom log levels
        self.add_custom_log_levels()



    
    def add_custom_log_levels(self):
        logging.addLevelName(USER_INPUT_LEVEL_NUM, "USER_INPUT")
        logging.addLevelName(ALERT_LEVEL_NUM, "ALERT")
        logging.addLevelName(IMPORTANT_LEVEL_NUM, "IMPORTANT")
        logging.addLevelName(ACTION_REQUIRED_LEVEL_NUM, "ACTION_REQUIRED")
        logging.addLevelName(MESSAGE_LEVEL_NUM, "MESSAGE")
        logging.addLevelName(EXCEPTION_LEVEL_NUM, "EXCEPTION")
        logging.Logger.user_input = self.user_input
        logging.Logger.alert = self.alert
        logging.Logger.important = self.important
        logging.Logger.action_required = self.action_required
        logging.Logger.message = self.message
        logging.Logger.exception = self.exception

    def info(self, message, *args, **kws) -> None:
        if self.isEnabledFor(logging.INFO):
            self.handle(self.makeRecord(name=self.log_name, level=logging.INFO, fn=inspect.stack()[1][1], lno=inspect.stack()[1][2], msg=message, args=args, exc_info=None, func=inspect.stack()[1][3]))
    
    def debug(self, message, *args, **kws) -> None:
        if self.isEnabledFor(logging.DEBUG):
            self.handle(self.makeRecord(name=self.log_name, level=logging.DEBUG, fn=inspect.stack()[1][1], lno=inspect.stack()[1][2], msg=message, args=args, exc_info=None, func=inspect.stack()[1][3]))

    def error(self, message, *args, **kws) -> None:
        if self.isEnabledFor(logging.ERROR):
            self.handle(self.makeRecord(name=self.log_name, level=logging.ERROR, fn=inspect.stack()[1][1], lno=inspect.stack()[1][2], msg=message, args=args, exc_info=None, func=inspect.stack()[1][3]))

    def critical(self, message, *args, **kws) -> None:
        if self.isEnabledFor(logging.CRITICAL):
            self.handle(self.makeRecord(name=self.log_name, level=logging.CRITICAL, fn=inspect.stack()[1][1], lno=inspect.stack()[1][2], msg=message, args=args, exc_info=None, func=inspect.stack()[1][3]))

    def exception(self, message, *args, **kws) -> None:
        if self.isEnabledFor(EXCEPTION_LEVEL_NUM):
            self.handle(self.makeRecord(name=self.log_name, level=EXCEPTION_LEVEL_NUM, fn=inspect.stack()[1][1], lno=inspect.stack()[1][2], msg=message, args=args, exc_info=None, func=inspect.stack()[1][3], exception=sys.exc_info()))
    
    def warning(self, message, *args, **kws) -> None:
        if self.isEnabledFor(logging.WARNING):
            self.handle(self.makeRecord(name=self.log_name, level=logging.WARNING, fn=inspect.stack()[1][1], lno=inspect.stack()[1][2], msg=message, args=args, exc_info=None, func=inspect.stack()[1][3]))
       
    def alert(self, message, *args, **kws) -> None:
        if self.isEnabledFor(ALERT_LEVEL_NUM):
            self.change_stream_log_format()
            self.handle(self.makeRecord(name=self.log_name, level=ALERT_LEVEL_NUM, fn=inspect.stack()[1][1], lno=inspect.stack()[1][2], msg=message, args=args, exc_info=None, func=inspect.stack()[1][3]))
            self.change_stream_log_format_to_default()
            
    def important(self, message, *args, **kws) -> None:
        if self.isEnabledFor(IMPORTANT_LEVEL_NUM):
            # changes output format for important messages with change_stream_log_format
            self.change_stream_log_format()
            self.handle(self.makeRecord(name=self.log_name, level=IMPORTANT_LEVEL_NUM, fn=inspect.stack()[1][1], lno=inspect.stack()[1][2], msg=message, args=args, exc_info=None, func=inspect.stack()[1][3]))
            # changes output format back to default
            self.change_stream_log_format_to_default()

    def user_input(self, message, *args, **kws) -> None:
        if self.isEnabledFor(USER_INPUT_LEVEL_NUM):
            self.handle(self.makeRecord(name=self.log_name, level=USER_INPUT_LEVEL_NUM, fn=inspect.stack()[1][1], lno=inspect.stack()[1][2], msg=message, args=args, exc_info=None, func=inspect.stack()[1][3]))

    def message(self, message, *args, **kws) -> None:
        if self.isEnabledFor(MESSAGE_LEVEL_NUM):
            self.change_stream_log_format()
            self.handle(self.makeRecord(name=self.log_name, level=MESSAGE_LEVEL_NUM, fn=inspect.stack()[1][1], lno=inspect.stack()[1][2], msg=message, args=args, exc_info=None, func=inspect.stack()[1][3]))
            self.change_stream_log_format_to_default()

    def action_required(self, message, *args, **kws) -> None:
        if self.isEnabledFor(ACTION_REQUIRED_LEVEL_NUM):
            self.change_stream_log_format()
            self.handle(self.makeRecord(name=self.log_name, level=ACTION_REQUIRED_LEVEL_NUM, fn=inspect.stack()[1][1], lno=inspect.stack()[1][2], msg=message, args=args, exc_info=None, func=inspect.stack()[1][3]))
            self.change_stream_log_format_to_default()

    def handle(self, record):
        super().handle(record)

    # makeRecord, format, and emit are the only methods that need to be overridden
    # if exception is not None, handle it
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, exception=None) -> logging.LogRecord:
        rv = logging.LogRecord(name, level, fn, lno, msg, args, exc_info, func, extra)
        if exception is not None:
            rv.exc_info = exception
        return rv

    # add console handler to the logger
    def add_console_handler(self, log_format=STREAM_LOG_DEFAULT_FORMAT, time_format=STREAM_DEFAULT_TIME_FORMAT, field_styles=STREAM_DEFAULT_FIELD_STYLES, level_styles=STREAM_DEFAULT_LEVEL_STYLES):
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setFormatter(coloredlogs.ColoredFormatter(log_format, time_format, field_styles=field_styles, level_styles=level_styles))
        self.addHandler(self.stream_handler)

    # add file handler to the logger, check if log directory exists, if not create it, if it exists, check if log file exists, if not create it, if it exists, append to it
    # log name contains current date
    def add_file_handler(self, file_name, log_format=DEFAULT_FILE_LOG_FORMAT, time_format=DEFAULT_FILE_TIME_FORMAT, field_styles=STREAM_DEFAULT_FIELD_STYLES, level_styles=STREAM_DEFAULT_LEVEL_STYLES):
        logdir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        log_file = os.path.join(logdir, file_name)
        # add date to log file name
        log_file = log_file + '_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        # create file handler
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setFormatter(logging.Formatter(log_format, time_format))
        self.addHandler(self.file_handler)

    # change stream log format to STREAM_LOG_LESSINFO_FORMAT
    def change_stream_log_format(self, log_format=STREAM_LOG_LESSINFO_FORMAT, time_format=STREAM_DEFAULT_TIME_FORMAT, field_styles=STREAM_DEFAULT_FIELD_STYLES, level_styles=STREAM_DEFAULT_LEVEL_STYLES):
        self.stream_handler.setFormatter(coloredlogs.ColoredFormatter(log_format, time_format, field_styles=field_styles, level_styles=level_styles))

    # change stream log format to STREAM_LOG_DEFAULT_FORMAT
    def change_stream_log_format_to_default(self, log_format=STREAM_LOG_DEFAULT_FORMAT, time_format=STREAM_DEFAULT_TIME_FORMAT, field_styles=STREAM_DEFAULT_FIELD_STYLES, level_styles=STREAM_DEFAULT_LEVEL_STYLES):
        self.stream_handler.setFormatter(coloredlogs.ColoredFormatter(log_format, time_format, field_styles=field_styles, level_styles=level_styles))


def main():
    log = CustomLog()
    log.user_input("user input TESTTEST")
    log.alert("alert TESTTEST")
    log.important("important TESTTEST")
    log.action_required("action required TESTTEST")
    log.message("message TESTTEST")
    log.info("info TESTTEST")
    log.debug("debug TESTTEST")
    log.warning("warning TESTTEST")
    log.error("error TESTTEST")
    log.critical("critical TESTTEST")

    try:
        raise Exception("test")
    except Exception as e:
        log.exception(e)


if __name__ == "__main__":
    main()