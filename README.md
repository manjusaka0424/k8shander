# Aliyun Kubernetes Manager

*实现阿里云Kubernetes服务调度功能，包括命名空间(Namespace)/部署(Deployment)/服务（Service）/Pod/Ingress查询、创建、删除等功能。*

## 截图 [链接](https://github.com/shijl0925/aliyun-kubernetes-manager/tree/master/screenshots)

## Features
* User registration, forgot password
* Database setup, including database migrations and CRUD examples
* Fast deployment on gunicorn and supervisor
* Powerful stack: back-end based on Python with Flask


## What's included?

* Blueprints
* flask-security for User and permissions management
* Flask-SQLAlchemy for databases

## How to install

```
$ pip3 install -r requirements.txt
```

## How to run
```
$ python3 -m flask --help # for help

$ export FLASK_DEBUG=1
$ export FLASK_APP=app.main
$ python3 -m flask initdb
$ python3 -m flask run
```

## How to Migrate database
```
$ python3 -m flask db init # create the database or enable migrations
$ python3 -m flask db migrate # generate an initial migration
$ python3 -m flask db upgrade # apply the migration to the database
```

Running on http://127.0.0.1:5000/apis/swagger

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
