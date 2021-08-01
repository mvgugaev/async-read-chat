import logging
import asyncio
import configargparse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sender')

def parse_arguments():
    """Функция обработки аргументов командной строки."""
    parser = configargparse.ArgParser(
        default_config_files=['write_config.conf',],
        description='Async app to read tcp chat.',
    )
    parser.add(
        '-ho', 
        '--host', 
        help='Server HOST',
        is_config_file=True,
        required=True,
    )
    parser.add(
        '-p', 
        '--port', 
        help='Server PORT',
        is_config_file=True,
        required=True,
    )
    parser.add(
        '-ha', 
        '--hash', 
        help='User hash',
        is_config_file=True,
        required=True,
    )
    return parser.parse_args()


async def write_to_socket(writer, data:str):
    """Метод для отправки текста в сокет."""
    writer.write(data.encode())
    logger.debug(data.rstrip())
    await writer.drain()

async def read_and_print_from_socket(reader):
    """Метод для чтения и вывода строки из сокета."""
    data = await reader.readline()
    logger.debug(data.decode().rstrip())

async def tcp_write_chat(host: str, port: str, hash: str):
    """Асинхронная функция для записи в чат."""
    reader, writer = await asyncio.open_connection(host, port)
    await read_and_print_from_socket(reader)
    await write_to_socket(writer, f'{hash}\n')
    await read_and_print_from_socket(reader)
    await read_and_print_from_socket(reader)
    await write_to_socket(
        writer,
        'Я снова тестирую чатик. Это третье сообщение.\n\n',
    )
    await read_and_print_from_socket(reader)

    logger.debug('Close the connection')
    writer.close()
    await writer.wait_closed()


def main():
    """Основная логика приложения."""
    args = parse_arguments()
    asyncio.run(tcp_write_chat(
        args.host,
        args.port,
        args.hash,
    ))

if __name__ == '__main__':
    main()
