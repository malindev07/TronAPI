# TronAPI
## Микросервис, который выводит информацию по адресу кошелька в сети Tron, его bandwidth, energy, и баланс trx


### Запуск

```bash
# Клонировать репозиторий
git clone https://github.com/malindev07/TronAPI.git
cd TronAPI

# Установка виртуального окружения и зависимостей
make install

# Запустить сервис
make run

# Запустить тесты
make test
```
> [!NOTE]
> Для отключения удаления данных из БД, при каждом запуске,
> поменять в .env <ins>DB_DROP=0</ins>
> для очистки БД при каждом запуске <ins>DB_DROP=1</ins>
 


## Что возвращает сервис

Если адрес кошелька валиден, сервис возвращает:
status_code = 200
```json
{
  "address": "TSJrqxMBCGxutmHk8immsLgqCXwHFMRhcS",
  "balance": 302.366723,
  "bandwidth": 24,
  "energy": 163917
}
```
Если адрес кошелька не существует сервис возвращает:
status_code = 404
```json
{
  "address": "TQAXVqxCHPGEAQMn925kta22FUicd28SLo",
  "msg": "Not found"
}
```

