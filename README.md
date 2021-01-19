# Описание приложения
<h2 align="center">Доска объявлений</h2>

БД:	

	https://app.dbdesigner.id/?action=open&uuid=102add70-68b8-4a20-acc7-88809f8b1832

Запуск проекта:

##### 1) Скопировать проект с помощью 

	git clone https://github.com/SergeyIntyashev/BulletinBoard

##### 2) В корневой папке через терминал запустить докер командой 
	
	docker-compose up --build

##### 3) Создать суперпользователя

    docker exec -it bulletinboard_web_1 python manage.py createsuperuser