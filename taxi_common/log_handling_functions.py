import sys
import logging


def get_logger():
    logger_name = '___log_%s' % sys.argv[0][:-len('.py')]
    logger = logging.getLogger('%s' % (logger_name))
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('%s.log' % (logger_name))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


# TODO
# Write error in logger