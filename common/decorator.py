import inspect
import sys
import logs.config_client_log
import logs.config_server_log
import logging

sys.path.append('../')

if sys.argv[0].find('client_dist') == -1:
    logger = logging.getLogger('server_dist')
else:
    logger = logging.getLogger('client_dist')


def log(func):
    def wrapper(*args, **kwargs):
        wrapped_func = func(*args, **kwargs)
        logger.debug(f'Была вызвана функция {func.__name__}(), '
                     # f'с параметрами {args} {kwargs}'
                     # f'вызов из модуля {func.__module__}'
                     # f'вызов из функции {traceback.format_stack()[0].strip().split()[-1]}'
                     f'вызов произошёл из функции {inspect.stack()[1][3]}()')
        return wrapped_func

    return wrapper
