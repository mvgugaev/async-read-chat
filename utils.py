import json
import configargparse

def get_json(data: str):
    """Конвертация строки в json"""
    try:
        return json.loads(data)
    except ValueError as e:
        return False


async def write_to_socket(writer, data:str, logger):
    """Метод для отправки текста в сокет."""
    writer.write(data.encode())
    logger.debug(data.rstrip())
    await writer.drain()


async def read_and_print_from_socket(reader, logger):
    """Метод для чтения и вывода строки из сокета."""
    data = (await reader.readline()).decode().rstrip()
    logger.debug(data)
    return data


async def close_connection(writer, logger):
    """Закрытие соединения с сокетом."""
    logger.debug('Close the connection')
    writer.close()
    await writer.wait_closed()


def parse_arguments(description: str, config_file: str, history_argument: bool = False):
    """Функция обработки аргументов командной строки."""
    parser = configargparse.ArgParser(
        default_config_files=[config_file,],
        description=description,
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
    if history_argument:
        parser.add(
            '-hi', 
            '--history', 
            help='File to store messages',
            is_config_file=True,
            required=True,
        )
    return parser.parse_args()
