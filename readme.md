# ВАЖНО! Как делаем наименования веток #
1. Заходим в ветку dev
2. Создаем новую ветку от dev &#8594; **dev/\[Название ветки\]**
3. Коммитим в эту ветку
4. Пишем в чат об изменениях или собираемся все вместе и делаем merge

# Инструкция по установке проекта #
1. Делаем git clone проекта
2. ПКМ по папке perforator &#8594; Open Folder as PyCharm Project
3. Проверьте, что у вас выбран интерпретатор Python (снизу справа)
4. Откройте терминал. Первый темринал называется Local, пока будем в нем работать

### Для Django

!!! Команды которые нужно выполнить в терминале Local:

1. ```cd backend```
2. ```virtualenv -p python3 env```
3. ```env/scripts/activate```
(После этой команды должна появиться надпись (env) перед PS C:\\)<br>
Пример: ![alt text](https://i.ibb.co/FnkJm7M/Screenshot-1.png)
4. ```pip install django djangorestframework```
5. ```pip install django-cors-headers```
6. ```python manage.py makemigrations api```
7. ```python manage.py migrate api```

### Настраиваем сессии в Django

!!! Команды нужно выполнить в том же терминале Local:

1. Убедитесь, что в ```api/settings.py``` массив ```INSTALLED_APPS = [ ... ]```
содержит строку ```'django.contrib.sessions'```
2. Убедитесь, что в том же файле ```api/settings.py``` массив ```MIDDLEWARE = [ ... ]```
содержит строку ```'django.contrib.sessions.middleware.SessionMiddleware'```
3. Выполните миграции для ```api``` из пунктов 6 и 7, расположенных выше, если еще
не сделали это
4. Выполните команду: ```python manage.py makemigrations``` (без ```api```)
5. Выполните команду: ```python manage.py migrate``` (без ```api```)
6. В базе данных должна появиться таблица с названием ```django_session```

### Для Vue.js

!!! Создайте новый терминал нажав "+" около Local. Повится терминал с названием Local (2). Следующие команды выполняем в нем:
1. ```cd frontend```
2. ```npm install```
3. ```npm install pug --save-dev```
4. ```npm install axios vue-axios --save```
5. ```npm install vuex --save```
6. ```npm audit fix```
## Запуск проекта ##
Запуск Django происходит в консоли Local, когда есть приставка (env). Если ее нет, нужно выполнить команду:
```env/scripts/activate```
<br>
Если (env) включено:
```python backend/manage.py runserver```
<br><br>
Запуск VueJS происходит в консоли Local (2): <br>
```cd frontend``` <br>
```npm run dev```
<br><br>
## Добавление новых модулей в Django: ##
1. ```cd backend```
2. ```django-admin startapp [название модуля]```
3. Затем новый модуль нужно добавить в список установленных приложений (INSTALLED_APPS):
```
# backend/api/settings.py

INSTALLED_APPS = [
    ...
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users',
    'corsheaders',
    '[название модуля]',
]
```
4. Создать модель
5. Выполнить миграцию:
* ```python backend/manage.py makemigrations```
* ```python backend/manage.py migrate```
