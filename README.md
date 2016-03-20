# Project: Suggesteur de cadeaux intelligents

Application Web et/ou Mobile axé sur le back-end permettant d'effectuer des recherches de cadeux à partir de critères dynamiques sur une base de donnée dont les informations sont recueillis sur des sites e-commerce par Web Scrapping et par API.


##Accounts:

App  | Username | password
------------- | ------------- | -------------
Gmail  | backslashzero8@gmail.com | backslash0
Facebook  | backslashzero8@gmail.com | backslash0



### Facebook app:
GiftSmarts - Test

**App ID:** 1670209469887605

**App Secret:** 65c27afa66f17051324f3a64243c7133


## Production

### Requirements
* Python 3.4+
* VirtualEnv 12.1+
* PostgreSQL 9.4

### Install
```
./install.sh
```

### Run
```
./run.sh
```

## Development

### Requirements
* Python 3.4+
* VirtualEnv 12.1+
* PostgreSQL 9.4
* NPM 2.8+
* Node 0.12+
* Grunt-CLI 0.1.13+
* Ruby 2.2+
* Nginx (optional)

### Install
```
./install-dev.sh
```

#### Install NLTK Corpus
```
./nltk-download.sh
```

Nginx config:
```
user www-data; # Nginx will be ran by this user, should NOT be root
worker_processes 4; # Number of core on the machine
pid /run/nginx.pid;

events {
    worker_connections 8096;
    multi_accept on;
    use epoll;
}

worker_rlimit_nofile 40000;

http {
    sendfile           on;
    tcp_nopush         on;
    tcp_nodelay        on;
    keepalive_timeout  15;

    server {
        listen 80;
        server_name test.flaskskeleton.com;

        location / {
            proxy_pass http://127.0.0.1:8333;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}

```

Nginx is used to better simulate the production environment, completely optional of course.

### Run
```
./run-dev.sh
```

### Assets compilation

Watches for modifications in assets:
```
grunt
```

### Access the shell

```
env/bin/python manage.py shell
```

### Creating Database

```
env/bin/python manage.py createDb
```

### Load fixtures

```
env/bin/python manage.py loadFixtures
```

### Create User

```
# From the Flask shell

from app.config.config import db
from app.models.user import *

UserActions.add_user("testteste", "Testtest12")
user = User.query.one()
user.active = True
db.session.commit()
```
