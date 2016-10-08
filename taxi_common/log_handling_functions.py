import logging


def get_logger(app_name):
    logger = logging.getLogger('%s' % (app_name))
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('%s.log' % (app_name))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger