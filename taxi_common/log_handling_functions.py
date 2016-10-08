import os, logging


def get_logger(app_name):
    logger = logging.getLogger('%s_%d' % (app_name, os.getpid()))
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('%s_%d.log' % (app_name, os.getpid()))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger