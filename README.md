API системы задач на Django Rest Framework +  Celery.

Функционал:
* создавать отделы
* создавать должности в отделах
* добавлять сотрудников в отделы
* менеджеры могут создавать проекты и задачи в  рамка проекта, менять статус проектов (закрыт, отменен, в ожидании, в работе)
* задача "падает" сотруднику на почту, в письме приходит информация о задаче и планируемом сроке ее выполнения
* сотрудник может создавать подзадачи для своей задачи, может менять ее статус (закрыта, отменена, в ожидании, в работе), также задачу может корреткировать руководитель сотрудника или менеджер
* рассчитывается активное и пассивное время работы над каждой задачей (например, если сотрудник зависим от подзадач и поставил ее на ожидание, а потом вернул в работу)
* каждый будний день в 6 утра запускается задача для celery-beat, celery рассылает по почте напоминания сотрудникам если скоро дедлайн задачи, или если задача была просрочена но не закрыта
* сотрудники видят все активные задачи и задачи в ожидании в своем профиле
* орагнизовано разграничение прав доступа
* Аутентификация по токенам (Djoser). 
* Для реализации возможности создавать подзадачи в рамках одной задачи Task-SubTasks использована библиотека django-mptt.
* Запросы должны содержать заголовок следующего вида: Authorization: Token <users token>
* Рассылка сообщений в почте через celery/celery-beat

1. ## Запуск
2. Клонируйте репозиторий
3. Запустите сборку командой: 
```shell
docker-compose up -d --build
```
4. Для просомтра журнала используйте:
```shell
docker-compose logs -f
```
5. Откройте http://0.0.0.0:8000/swagger-ui/ для просмотра документации Swagger



| endpoint                     | description                                                                                                                                                                               | field                                                                                    | methods                 |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|-------------------------|
| api/company/                 | Список департаментов (отделов)                                                                                                                                                            | name, description, url (to detail about department)                                      | GET, POST               |
| api/company/{id}/            | Информация об отделе, список названий должностей  (roles) и сотрудников (employees) в должностях  c краткой инфо о сотруднике и ссылкой "company/user/{id}" на профиль каждого сотрудника | name, description, roles(-employees short info)                                          | GET, PUT, PATCH, DELETE |
| api/company/{id}/roles/      | Список должностей с инфо о сотрудниках и ссылками на должности "company/roles/{id}"                                                                                                       | name, description, roles(-employees short info)                                          | GET, POST               |
| api/company/roles/{id}/      | Информация о должности                                                                                                                                                                    | name, description, roles(-employees short info)                                          | GET, PUT, PATCH, DELETE |
| api/company/users/{id}/      | Подробная информация о пользователе с ссылкой на должность "company/roles/{id}"                                                                                                           | first_name, last_name, email, birthday, gender, phone, role                              | GET, PUT, PATCH, DELETE |
| api/company/users/           | Список всех пользователей с краткой инфо                                                                                                                                                  | first_name, last_name, email, role, 'url'                                                | GET                     |
|                              |                                                                                                                                                                                           |                                                                                          |                         |
| api/task/projects/           | Список всех проектов, создание новых проектов если есть права менеджера                                                                                                                   | name, description, priority, planned_date, status, manager                               | GET, POST               |
| api/task/projects/{id}/      | Информация о проекте, о задачах в рамках проекта, возможность изменить статус (закрыть) проект, поставить на ожидание и тд.                                                               | name, description, priority, planned_date, status, manager, start_date, tasks[]          | GET, PUT, PATCH, DELETE |
| api/task/projects/{id}/tasks | Список задач в рамках проекта, создание задач, выбор исполнителя задачи                                                                                                                   | name, description, priority, planned_date, status, executor, start_date, project         | GET, POST               |
| api/task/{id}/               | Полная иформация о задаче, возможность сменить статус(закрыть, в ожидание), содержит ссылки на подзадачи и родительсике задачи task/{id} если они есть                                    | name, description, priority, planned_date, status, executor, start_date, project, parent | GET, PUT, PATCH, DELETE |
| api/task/{id}/delegate/      | Список подзадач, создание подзадачи                                                                                                                                                       | name, description, priority, planned_date, status, executor, start_date, project, parent | GET, POST               |
|                              |                                                                                                                                                                                           |                                                                                          |                         |
| api/auth/users/              | Регистрация нового пользователя                                                                                                                                                           | first_name, last_name, email, password                                                   | GET, POST               |
| api/auth/token/login/        | Получить токен для пользователя, если данные введены правильно - вернет "auth_token": "7...84"                                                                                            | email, password                                                                          | POST                    |
| api/auth/token/logout/       | Удалить токен пользователя                                                                                                                                                                | Заголовок: Authorization:  Token <your token>                                            | GET                     |
| api/auth/users/me/           | Узнать пользователя по токену                                                                                                                                                             | Заголовок: Authorization:  Token <your token>                                            | GET                     |
