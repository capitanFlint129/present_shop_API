# present_shop_API
RESTful API для магазина подарков
# Установка
1) Обновляем пакеты:
    sudo apt-get update
    sudo apt-get upgrade
2) Устанавливаем необходимые пакеты:
    sudo apt-get install mysql-server python-mysqldb python-profiler w3m python-setuptools libmysqlclient-dev python-dev supervisor nginx
    sudo apt install python3-pip
    pip3 install mysqlclient
# Развертывание
1) Установим virtualenv:
    pip3 install virtualenv
2) Создаем папку с проектом и виртуальной средой:
    mkdir backend_school_project
    cd backend_school_project
    mkdir present_shop_API
    cd present_shop_API
    git clone https://github.com/capitanFlint129/present_shop_API.git /home/entrant/backend_school_project
3) Создаем вирутальную среду, активируем ее и скачиваем нужные пакеты:
    virtualenv env
    source /home/entrant/backend_school_project/env/bin/activate
    cd present_shop_API
    pip install -r requirements.txt
4) Создаем базу данных:
    sudo mysql -u root -p
    CREATE DATABASE psa CHARACTER SET utf8 COLLATE utf8_general_ci;
    CREATE USER 'psa_user'@'localhost' IDENTIFIED BY '123';
    GRANT ALL PRIVILEGES ON psa.* TO 'psa_user'@'localhost';
    exit
5) Создаем таблицы:
    cd psa
    /home/entrant/backend_school_project/env/bin/python manage.py makemigrations
    /home/entrant/backend_school_project/env/bin/python migrate
6) Удаляем дефолтные конфиги nginx и создаем свой:
    sudo rm -rf /etc/nginx/sites-enabled/default
    sudo rm -rf /etc/nginx/sites-available/default
    sudo ln -sf /home/entrant/backend_school_project/present_shop_API/etc/nginx.conf  /etc/nginx/nginx.conf
    sudo service nginx restart
7) Настраиваем gunicorn и supervisor:
    sudo ln -sf /home/entrant/backend_school_project/present_shop_API/etc/psa.conf /etc/supervisor/conf.d/psa.conf
    sudo update-rc.d supervisor enable
    sudo service supervisor start
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl status psa
# Запуск тестов
Для запуска тестов необходимо:
1) Дать права:
    sudo mysql -u root -p
    GRANT ALL PRIVILEGES ON test_psa.* TO 'psa_user'@'localhost';
2) Находясь в директории /home/entrant/backend_school_project/present_shop_API/psa, активировать виртуальную среду и выполнить следующую команду:
    python manage.py test
