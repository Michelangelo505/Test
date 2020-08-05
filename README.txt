Автор:
 	Поздняков М.А
Email:
	garrys505@gmail.com 

Описание:
	Проект находится в репозитории https://github.com/Michelangelo505/Test,
	образ проекта для docker находится в репозитории 
	https://hub.docker.com/repository/docker/michelangelo505/django_test,
	для запуска приложения используется docker-compose
Установка: 
	- Для того чтобы установить приложение, необходимо скачать docker и docker-compose
	- Скачать из папки install проекта файл docker-compose.yml
	- Зайти в терминал и перейти в директорию где находится файл docker-compose.yml
	- применить команду docker-compose pull (В Linux возможно потребуется root права,
	  необходимо написать sudo docker-compose pull). Docker загрузит необходимый образ
	  из https://hub.docker.com/repository/docker/michelangelo505/django_test.
Запуск:
	Выполнив все действия выше, можно запустить приложение с помощью команды
	docker-compose up (или sudo docker-compose up).
Работа приложения:
	Для работы приложения используйте http-client postman (или аналогичный ему)
	Get запрос по url http://127.0.0.1:8000/api/customers/ возращает список
	из 5 клиентов, потративших наибольшую сумму за весь период.
	Для отправки Post запроса по url http://127.0.0.1:8000/api/customers/
	необходимо в аргумент deals прикрепить файл содержащий историю сделок.
	Возращает Status: Ok, если файл был получен и обработан успешно, 
	иначе 'Status':'Error','Desc':<описание ошибки>'.
	
	

	
