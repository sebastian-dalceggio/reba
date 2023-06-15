import logging


def get_logger(name, level="INFO"):
    """
    Function to get a Python logger. It can be used for different objects to share the same logger.

    Parameters
    ----------
    name : string
        logger file name
    leve : string, default INFO
        debugger level

    Returns
    -------
    logger : python logger
        Return a python logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    file_handler = logging.FileHandler("logger/logging.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
