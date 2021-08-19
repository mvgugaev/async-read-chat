import json
import asyncio
from pathlib import Path
import configargparse
from contextlib import asynccontextmanager


def convert_string_to_json(data: str) -> tuple:
    """Конвертация строки в json -> (status, result)"""
    try:
        return True, json.loads(data)
    except ValueError as e:
        return False, None


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

@asynccontextmanager
async def open_connection(host: str, port: int, logger):
    """Контекстный менеджер для открытия tcp соединения"""
    reader, writer = await asyncio.open_connection(host, port)
    try:
        yield reader, writer
    finally:
        await close_connection(writer, logger)
