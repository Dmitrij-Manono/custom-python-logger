from helpers.custom_log import CustomLog
import test_app

def test_custom_log():
    log = CustomLog()
    log.info("This is a test")
    log.debug("This is a test")
    log.warning("This is a test")
    log.error("This is a test")
    log.critical("This is a test")
    log.user_input("This is a test")
    log.action_required("This is a test")
    log.alert("This is a test")
    log.important("This is a test")
    log.message("This is a test")


    try:
        raise Exception('This is an exception')
    except Exception as e:
        log.exception(e)

if __name__ == '__main__':
    test_custom_log()
    test_app.test_custom_log()
