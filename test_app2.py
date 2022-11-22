import test_app
from helpers.custom_loggers import CustomLogger

test_app.main()


log = CustomLogger(log_name="test_app2")
log.info("This is an info message")
log.warning("This is a warning message")
log.alert("This is an alert message")

