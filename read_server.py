import datetime
import logging
import asyncio
import aiofiles
from pathlib import Path
from utils import (
    close_connection, 
    read_and_print_from_socket,
    parse_arguments,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('reader')


async def tcp_read_chat(backup_file_name: str, host: str, port: str):
    """Асинхронная функция для чтения чата с удаленного сервера."""
    reader, writer = await asyncio.open_connection(host, port)

    async with aiofiles.open(Path(backup_file_name), mode='a') as backup_file:
        while not reader.at_eof():
            data = await read_and_print_from_socket(reader, logger)
            date_string = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
            await backup_file.write(f'[{date_string}] {data}')
            await asyncio.sleep(1)

    await close_connection(writer, logger)


def main():
    """Основная логика приложения."""
    args = parse_arguments(
        'Async app to read tcp chat.',
        'read_config.conf',
        history_argument=True,
    )
    asyncio.run(tcp_read_chat(
        args.history,
        args.host,
        args.port,
    ))

if __name__ == '__main__':
    main()
