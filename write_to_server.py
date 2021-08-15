import logging
import asyncio
import aiofiles
from utils import (
    get_json, 
    write_to_socket, 
    read_and_print_from_socket,
    close_connection,
    parse_arguments,
)

TOKEN_FILE = 'token.txt'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sender')


async def tcp_write_chat(host: str, port: str, token_file: str):
    """Асинхронная функция для записи в чат."""
    reader, writer = await asyncio.open_connection(host, port)
    await read_and_print_from_socket(reader, logger)

    hash = ''
    async with aiofiles.open(token_file, mode='r') as token_file:
        hash = await token_file.read()

    await write_to_socket(writer, f'{hash.rstrip()}\n', logger)
    data = await read_and_print_from_socket(reader, logger)

    if not get_json(data):
        await close_connection(writer, logger)
        logger.debug('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        return

    await read_and_print_from_socket(reader, logger)
    await write_to_socket(
        writer,
        'Я снова тестирую чатик. Это третье сообщение.\n\n',
        logger,
    )
    await read_and_print_from_socket(reader, logger)
    await close_connection(writer, logger)


def main():
    """Основная логика приложения."""
    args = parse_arguments(
        'Async app to write message to tcp chat.',
        'write_config.conf',
    )
    asyncio.run(tcp_write_chat(
        args.host,
        args.port,
        TOKEN_FILE,
    ))

if __name__ == '__main__':
    main()
