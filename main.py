import asyncio

BACKUP_FILE_NAME = 'messages.txt'
SERVER_ADDRESS = 'minechat.dvmn.org'
SERVER_PORT = 5000

async def tcp_read_chat(backup_file_name: str, server_address: str, server_port: str):
    """Асинхронная функция для чтения чата с удаленного сервера."""
    reader, writer = await asyncio.open_connection(
        server_address, server_port)

    with open(backup_file_name, 'a') as backup_file:
        while not reader.at_eof():
            data = await reader.readuntil(separator=b'\n')
            backup_file.write(data.decode())
            await asyncio.sleep(1)

    print('Close the connection')
    writer.close()


def main():
    """Основная логика приложения."""
    asyncio.run(tcp_read_chat(
        BACKUP_FILE_NAME,
        SERVER_ADDRESS,
        SERVER_PORT,
    ))

if __name__ == '__main__':
    main()
