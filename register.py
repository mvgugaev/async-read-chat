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


async def tcp_register_in_chat(host: str, port: str, token_file: str):
    """Асинхронная функция для регистрации в чате."""
    reader, writer = await asyncio.open_connection(host, port)
    await read_and_print_from_socket(reader, logger)
    await write_to_socket(writer, '\n', logger)
    await read_and_print_from_socket(reader, logger)
    name = input("Имя пользователя:")
    await write_to_socket(writer, f'{name}\n', logger)

    data = await read_and_print_from_socket(reader, logger)
    hash = get_json(data)['account_hash']

    async with aiofiles.open(token_file, mode='w') as token_file:
        await token_file.write(hash)

    await close_connection(writer, logger)


def main():
    """Основная логика приложения."""
    args = parse_arguments(
        'Async app to register in chat.',
        'write_config.conf',
    )
    asyncio.run(tcp_register_in_chat(
        args.host,
        args.port,
        TOKEN_FILE,
    ))


if __name__ == '__main__':
    main()
