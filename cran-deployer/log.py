import logging


def setup(debug=False):
    formatter_str = '%(asctime)s %(levelname)s %(message)s'
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(formatter_str))

    logger = logging.getLogger(__name__)
    logger.addHandler(handler)

    log_level = logging.DEBUG if debug else logging.INFO
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    logging.logThreads = 0
    logging.logProcesses = 0


def add_file_logger(logfile):
    if logfile:
        file_formatter_str = '%(asctime)s %(levelname)s %(message)s'
        file_handler = logging.FileHandler(logfile, mode='w')
        file_handler.setFormatter(logging.Formatter(file_formatter_str))
        logger = logging.getLogger(__name__)
        logger.addHandler(file_handler)


LOG = logging.getLogger(__name__)
