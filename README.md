## Описание:
Финальный проект для модуля Яндекс Практикума "API: интерфейс взаимодействия программ". В нём реализована REST API для сервиса Yatube (социальная сеть, в которой можно публиковать посты) по заранее подготовленной документации. REST API обеспечивает взаимодействие между клиентом и сервером через стандартные HTTP-запросы для обмена данными, польза которого заключается в простоте, масштабируемости и универсальности.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/yandex-praktikum/kittygram_backend.git
```
```
cd kittygram_backend
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
* Если у вас Linux/macOS
    ```
    source env/bin/activate
    ```
* Если у вас windows
    ```
    source env/scripts/activate
    ```
```
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```

## Примеры:

Полную документацию можно найти при запуске проекта по пути redoc/

### 1. Получение списка публикаций с пагинацией
```http
GET /api/v1/posts/?limit=10&offset=20 HTTP/1.1
Host: api.example.org
Accept: application/json
```

**Описание**:  
Запрос возвращает 10 публикаций, начиная с 21-й (offset=20 означает пропустить первые 20 записей).

**Пример ответа**:
```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=30&limit=10",
  "previous": "http://api.example.org/accounts/?offset=10&limit=10",
  "results": [
    {
      "id": 21,
      "author": "user1",
      "text": "Текст публикации...",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": null,
      "group": 1
    }
  ]
}
```

---

### 2. Создание новой публикации
```http
POST /api/v1/posts/ HTTP/1.1
Host: api.example.org
Authorization: Bearer your_access_token_here
Content-Type: application/json

{
  "text": "Новый пост в блоге",
  "group": 1
}
```

**Описание**:  
Создает новую публикацию. Требуется аутентификация. Поле `text` обязательно.

**Пример успешного ответа (201 Created)**:
```json
{
  "id": 124,
  "author": "current_user",
  "text": "Новый пост в блоге",
  "pub_date": "2023-05-20T15:30:00.000Z",
  "image": null,
  "group": 1
}
```

---

### 3. Получение JWT-токена
```http
POST /api/v1/jwt/create/ HTTP/1.1
Host: api.example.org
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Описание**:  
Запрос для получения JWT-токена (access и refresh).

**Пример успешного ответа (200 OK)**:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
