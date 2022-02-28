import inspect
import sys
import logs.config_client_log
import logs.config_server_log
import logs.config_client_log
import socket
import logging
import sys

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


def login_required(func):
    def checker(*args, **kwargs):
        from server.core import MessageProcessor
        from common.variables import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            if not found:
                raise TypeError
        return func(*args, **kwargs)
    return checker
