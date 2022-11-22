import test_app
from helpers.custom_logger import CustomLogger

test_app.main()


log = CustomLogger(log_name="test_app2")
log.create_file_handler()
log.info("This is an info message")
log.warning("This is a warning message")
log.alert("This is an alert message")
log.important("This is an important message")
log.error("This is an error message")
log.debug("This is a debug message")
log.critical("This is a critical message")
log.input_required("This is an input required message")
