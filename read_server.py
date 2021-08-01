import datetime
import asyncio
import aiofiles
import configargparse
from pathlib import Path


def parse_arguments():
    """Функция обработки аргументов командной строки."""
    parser = configargparse.ArgParser(
        default_config_files=['read_config.conf',],
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
        '-hi', 
        '--history', 
        help='File to store messages',
        is_config_file=True,
        required=True,
    )
    return parser.parse_args()


async def tcp_read_chat(backup_file_name: str, host: str, port: str):
    """Асинхронная функция для чтения чата с удаленного сервера."""
    reader, writer = await asyncio.open_connection(host, port)

    async with aiofiles.open(Path(backup_file_name), mode='a') as backup_file:
        while not reader.at_eof():
            data = await reader.readuntil(separator=b'\n')
            date_string = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
            print(data.decode())
            await backup_file.write(f'[{date_string}] {data.decode()}')
            await asyncio.sleep(1)

    print('Close the connection')
    writer.close()


def main():
    """Основная логика приложения."""
    args = parse_arguments()
    asyncio.run(tcp_read_chat(
        args.history,
        args.host,
        args.port,
    ))

if __name__ == '__main__':
    main()
