import json
from pathlib import Path
import configargparse

def convert_string_to_json(data: str):
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


def get_parser(description: str, config_file: str):
    """Функция для генерации парсера аргументов командной строки."""
    return configargparse.ArgParser(
        default_config_files=[
            str(Path.cwd() / 'configs' / config_file),
        ],
        description=description,
    )
