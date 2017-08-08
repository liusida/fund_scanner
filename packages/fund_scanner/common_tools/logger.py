import logging
import datetime as dt
import os

# find the root directory of the project 
path = os.path.join( os.path.dirname(os.path.abspath( os.path.join(__file__,os.pardir,os.pardir,os.pardir))), 'logs/', dt.datetime.today().strftime("%Y-%m-%d")+'.log')

logging.basicConfig(filename=path, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

logger = logging.getLogger()
def n():
    handler = logging.FileHandler(path)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Logging using decoration
def enter_exit_logger(func):
    def wrapper_function(*args, **kwargs):
        _logger = logging.getLogger('my_test')
        _logger.debug('Started: %s' % func.__name__)
        _logger.debug('args: {}, {}'.format(args,kwargs))
        init_time = dt.datetime.now()
        ret = func(*args, **kwargs)
        _logger.debug('Finished: %s in: %s seconds' % (func.__name__, dt.datetime.now() - init_time))
        return ret
    return wrapper_function


if __name__=='__main__':
    @enter_exit_logger
    def test_function(self):
        return
    test_function('a')