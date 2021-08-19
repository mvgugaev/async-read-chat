import datetime
import logging
import asyncio
import aiofiles
from pathlib import Path
from utils import (
    close_connection, 
    read_and_print_from_socket,
    get_parser,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('reader')


def parse_arguments():
    """Функция обработки аргументов командной строки."""
    parser = get_parser(
        'Async app to read tcp chat.',
        'read_config.conf',
    )
    parser.add_arg(
        '-ho', 
        '--host', 
        help='Server HOST',
    )
    parser.add_arg(
        '-p',
        '--port', 
        help='Server PORT',
    )
    parser.add_arg(
        '-hi', 
        '--history', 
        help='File to store messages',
    )
    return parser.parse_args()


async def read_tcp_chat(history_file_name: str, host: str, port: str):
    """Асинхронная функция для чтения чата с удаленного сервера."""
    reader, writer = await asyncio.open_connection(host, port)

    async with aiofiles.open(Path(history_file_name), mode='a') as history_file:
        while not reader.at_eof():
            data = await read_and_print_from_socket(reader, logger)
            date_string = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
            await history_file.write(f'[{date_string}] {data}')
            await asyncio.sleep(1)

    await close_connection(writer, logger)


def main():
    """Основная логика приложения."""
    args = parse_arguments()
    asyncio.run(read_tcp_chat(
        args.history,
        args.host,
        args.port,
    ))

if __name__ == '__main__':
    main()
