# Инстркция по установке проекта #
1. Зайдите в ветку frontend
2. Нажмите на кнопку Code (справа сверху)
3. Далее нажмите на Download ZIP
4. Разархивируйте в любое удобное место
5. ПКМ по папке perforator-frontend &#8594; Open Folder as PyCharm Project
6. Проверьте, что у вас выбран интерпретатор Python 3.10 (снизу справа)
7. Откройте терминал. Первый темринал называется Local, пока будем в нем работать

!!! Команды которые нужно выполнить в терминале Local:
8. ```virtualenv -p python3 env```
9. ```env/scripts/activate```
(После этой команды должна появиться надпись (env) перед PS C:\\)<br>
Пример: ![alt text](https://i.ibb.co/FnkJm7M/Screenshot-1.png)
10. ```pip install django djangorestframework```
11. ```pip install django-cors-headers```
12. ```python backend/manage.py migrate```

!!! Создайте новый терминал нажав "+" около Local. Повится терминал с названием Local (2). Следующие команды выполняем в нем:
13. ```cd frontend```
14. ```npm install```
15. ```npm install pug --save-dev```
16. ```npm install axios vue-axios --save```
17. ```npm install vuex --save```
18. ```npm audit fix```
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
##Добавление новых модулей в Django: ##
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