# Async chat control
Асинхронное приложение для работы с tcp чатом, которое поддерживает регистрацию, отправку сообщения и чтение из чата. Развернуть проект:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Регистрация
```
python3 register.py -ho minechat.dvmn.org -p 5050 -n my_name
```
Базовые настройки можно изменить в файле configs/write_config.conf

### Отправка сообщения
```
python3 write_to_server.py -ho minechat.dvmn.org -p 5050 -m my_message
```
Базовые настройки можно изменить в файле configs/write_config.conf

### Чтение сообщений
```
python3 read_server.py -ho minechat.dvmn.org -p 5050 -hi minechat.history
```
Базовые настройки можно изменить в файле configs/read_config.conf
