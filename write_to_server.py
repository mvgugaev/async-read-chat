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

TOKEN_FILE = 'token.txt'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sender')


def parse_arguments():
    """Функция обработки аргументов командной строки."""
    parser = get_parser(
        'Async app to write message to tcp chat.',
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
        '-m',
        '--message', 
        help='Message',
        required=True,
    )
    parser.add_arg(
        '-t',
        '--token', 
        help='User token',
    )
    return parser.parse_args()


async def authorise(reader, writer, token: str, logger):
    """Асинхронная функция для авторизации в чате."""
    await write_to_socket(writer, f'{token.rstrip()}\n', logger)
    data = await read_and_print_from_socket(reader, logger)

    if not convert_string_to_json(data):
        logger.debug('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        return False
    
    await read_and_print_from_socket(reader, logger)
    return True

async def submit_message(reader, writer, message:str, logger):
    """Асинхронная функция для отправки сообщения в чат."""
    await write_to_socket(
        writer,
        '{}\n\n'.format(message.replace("\n", "\\n")),
        logger,
    )
    await read_and_print_from_socket(reader, logger)

async def write_tcp_chat(host: str, port: str, message: str, token: str, token_file: str):
    """Асинхронная функция для записи в чат."""
    reader, writer = await asyncio.open_connection(host, port)
    await read_and_print_from_socket(reader, logger)

    if not token:
        async with aiofiles.open(token_file, mode='r') as token_file:
            token = await token_file.read()

    is_authorised = await authorise(reader, writer, token, logger)

    if not is_authorised:
        await close_connection(writer, logger)
        return

    await submit_message(
        reader, 
        writer,
        message,
        logger,
    )
    await close_connection(writer, logger)


def main():
    """Основная логика приложения."""
    args = parse_arguments()
    asyncio.run(write_tcp_chat(
        args.host,
        args.port,
        args.message,
        args.token,
        TOKEN_FILE,
    ))

if __name__ == '__main__':
    main()
