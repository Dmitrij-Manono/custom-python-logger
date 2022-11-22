from helpers.custom_loggers import ConsoleLogger



stream_logger = ConsoleLogger()
stream_logger.add_file_handler()
stream_logger.info("This is an info2 message")



def main():
    stream_logger.info("This is an info message")
    stream_logger.alert("This is an alert message")
    stream_logger.important("This is a stream logger")
    stream_logger.warning("This is a stream logger")
    stream_logger.error("This is a stream logger")
    stream_logger.debug("This is a stream logger")
    stream_logger.critical("This is a stream logger")
    #print(stream_logger.custom_find_caller())
    try:
        raise Exception("This is a test")
    except Exception as e:
        stream_logger.exception(e)
    #<class 'inspect.FrameInfo'>
    #print(stream_logger.find_caller())
    test()


def test():
    stream_logger.info("This is an info message")
    

if __name__ == "__main__":
    main()
    


