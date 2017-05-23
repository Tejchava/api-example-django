# drchrono Hackathon

### Requirements
- [pip](https://pip.pypa.io/en/stable/)
- [python virtual env](https://packaging.python.org/installing/#creating-and-using-virtual-environments)

### Setup
``` bash
Instructions to run the Project:
1. pip install -r requirements.txt
2. python manage.py makemigrations drchrono
3. python manage.py sqlmigrate drchrono 0001
4. python manage.py migrate
5. python manage.py runserver

Parallelly we should also run the rabbitmq-server and also run the
“celery -A drchrono worker --loglevel=info --beat”
```

`social_auth_drchrono/` contains a custom provider for [Python Social Auth](http://psa.matiasaguirre.net/) that handles OAUTH for drchrono. To configure it, set these fields in your `drchrono/settings.py` file:

```
SOCIAL_AUTH_DRCHRONO_KEY
SOCIAL_AUTH_DRCHRONO_SECRET
SOCIAL_AUTH_DRCHRONO_SCOPE
LOGIN_REDIRECT_URL
```
