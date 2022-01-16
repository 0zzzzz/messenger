import json
import socket
import sys
import time
import argparse
import logging
import logs.config_client_log
from errors import ReqFieldMissingError
from common.utils import send_message, get_message
from common.variables import *

CLIENT_LOGGER = logging.getLogger('client')


class Client:
    @staticmethod
    def create_presence(account_name='Guest'):
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            }
        }
        CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
        return out

    @staticmethod
    def process_ans(message):
        CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            return f'400 : {message[ERROR]}'
        raise ReqFieldMissingError(RESPONSE)

    @staticmethod
    def create_arg_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
        parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
        return parser

    def main(self):
        parser = self.create_arg_parser()
        namespace = parser.parse_args(sys.argv[1:])
        server_address = namespace.addr
        server_port = namespace.port
        if not 1023 < server_port < 65536:
            CLIENT_LOGGER.critical(f'Попытка запуска клиенте с неподходящим номером порта {server_port}. '
                                   f'Допустимы адреса с 1024 до 65535. Клиент завершиет работу')
            sys.exit(1)
        CLIENT_LOGGER.info(f'Запущен клиент с параметрами: '
                           f'адресс сервера: {server_address}, порт: {server_port}')
        try:
            transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            transport.connect((server_address, server_port))
            message_to_server = self.create_presence()
            send_message(transport, message_to_server)
            answer = self.process_ans(get_message(transport))
            CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
            print(answer)
        except json.JSONDecodeError:
            CLIENT_LOGGER.error(f'Не удалось декодировать полученную JSON строку')
        except ConnectionRefusedError:
            CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                                   f'конечный компьютер отверг запрос на подключение')
        except ReqFieldMissingError as missing_error:
            CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                                f'{missing_error.missing_field}')


if __name__ == '__main__':
    client_call = Client()
    client_call.main()
