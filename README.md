Для автоматизации процессов в веб-приложении «Инцидент-менеджмент» https://im.mlg.ru/
были разработаны скрипты, которые используют «скрытый API» для выполнения различных действий по работе с объектами в системе.  

Данные скрипты ранее вручную запускались на сервере, было необходимо обновлять пароль вручную и требовались навыки работы с командной строкой.  
Чтобы решить эти задачи был создан телеграм-бот, который предоставляет понятный пользовательский интерфейс с доступом ко всем скриптам и возможность обновлять пароль от учетной записи.

Проект разработан с учетом дальнейшего развития и подключения новых модулей. 
Процесс авторизации был выведен в отдельный модуль, данные о пользователях и токен хранятся в Redis до момента истечения срока валидности.
