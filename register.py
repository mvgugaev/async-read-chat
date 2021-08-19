import logging
import asyncio
import aiofiles
from utils import (
    convert_string_to_json, 
    write_to_socket, 
    read_and_print_from_socket,
    close_connection,
    get_parser,
)

TOKEN_FILE_NAME = 'token.txt'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sender')


def parse_arguments():
    """Функция обработки аргументов командной строки."""
    parser = get_parser(
        'Async app to register in chat.',
        'write_config.conf',
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
        '-n',
        '--name', 
        help='User name',
    )
    parser.add_arg(
        '-hi', 
        '--history', 
        help='File to store messages',
    )
    return parser.parse_args()


async def register(host: str, port: str, name: str, token_file_name: str):
    """Асинхронная функция для регистрации в чате."""
    reader, writer = await asyncio.open_connection(host, port)
    await read_and_print_from_socket(reader, logger)
    await write_to_socket(writer, '\n', logger)
    await read_and_print_from_socket(reader, logger)

    if not name:
        name = input("Имя пользователя:")
        
    await write_to_socket(
        writer, 
        '{}\n'.format(name.replace("\n", "\\n")), 
        logger,
    )

    response = await read_and_print_from_socket(reader, logger)
    convertation_status, json_response = convert_string_to_json(response)
    if not convertation_status or not json_response:
        logger.debug('Не удалось получить токен. Повторите попытку.')
        await close_connection(writer, logger)
        return False

    hash = json_response['account_hash']

    async with aiofiles.open(token_file_name, mode='w') as token_file:
        await token_file.write(hash)

    await close_connection(writer, logger)


def main():
    """Основная логика приложения."""
    args = parse_arguments()
    asyncio.run(register(
        args.host,
        args.port,
        args.name,
        TOKEN_FILE_NAME,
    ))


if __name__ == '__main__':
    main()
