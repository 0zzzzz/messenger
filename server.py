import json
import socket
import sys
from common.utils import get_message, send_message
from common.variables import *


class Server:
    @staticmethod
    def process_client_message(message):
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message \
                and message[USER][ACCOUNT_NAME] == 'Guest':
            return {RESPONSE: 200}
        return {
            RESPONSE: 400,
            ERROR: 'Bad Request' 
        }

    def main(self):
        try:
            if '-p' in sys.argv:
                listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            else:
                listen_port = DEFAULT_PORT
            if listen_port < 1024 or listen_port > 65535:
                raise ValueError
        except IndexError:
            print('После параметра -\'p\' необходимо указать номер порта')
            sys.exit(1)
        except ValueError:
            print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535')
            sys.exit(1)

        try:
            if '-a' in sys.argv:
                listen_address = sys.argv[sys.argv.index('-a') + 1]
            else:
                listen_address = ''
        except IndexError:
            print('Послу параметра -\'a\' необходимо указать адрес, который будет слушать ')
            sys.exit(1)

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((listen_address, listen_port))
        transport.listen(MAX_CONNECTIONS)

        while True:
            client, client_address = transport.accept()
            try:
                message_from_client = get_message(client)
                print(message_from_client)
                response = self.process_client_message(message_from_client)
                send_message(client, response)
                client.close()
            except (ValueError, json.JSONDecodeError):
                print('Принято некорректное сообщене от клиента')
                client.close()


if __name__ == '__main__':
    server_start = Server()
    server_start.main()
