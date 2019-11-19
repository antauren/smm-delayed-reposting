# SMM планировщик

Работа с Google Sheets 

Код достает статьи и изображения из Google Drive
публикует их по расписанию в социальных сетях 



## Чтобы запустить, потребуются следующие данные

* файл `credentials.json` (для работы с [Google Sheets API])  
* файл `client_secrets.json` (для работы с Google Drive API через [PyDrive])  
* токены и айди групп соц.сетей, например:  
    * `FACEBOOK_TOKEN`, `FACEBOOK_GROUP_ID` 
    * `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`
    * `VKONTAKTE_TOKEN`,`VKONTAKTE_GROUP_ID`


### Как запустить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

1. Создайте в корневой папке файл ```.env```
пропишите в нем токены и айди групп,
а также название таблицы на гугл-диске и диапозон ячеек с данными:  
    ```
    TELEGRAM_TOKEN=12345
    TELEGRAM_CHAT_ID=12345

    FACEBOOK_TOKEN=12345
    FACEBOOK_GROUP_ID=12345

    VKONTAKTE_TOKEN=12345
    VKONTAKTE_GROUP_ID=12345
   
    TITLE=Расписание публикаций ноябрь
    RANGE=A2:H
    ```
   
2. положите в корневую папку файлы: `credentials.json`, `client_secrets.json`

3. Запустите ```python main.py```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

[Google Sheets API]: https://www.youtube.com/watch?v=Bf8KHZtcxnA
[PyDrive]: https://gsuitedevs.github.io/PyDrive/docs/build/html/quickstart.html#authentication