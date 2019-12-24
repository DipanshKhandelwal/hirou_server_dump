# hirou

Route collection system for Field Protect

* Make sure you have [`pip`](https://pip.pypa.io/en/stable/installing/) installed in the system.

* Install [`pipenv`](https://github.com/pypa/pipenv) for managing dependencies for the project.

## Run project

* To start virtual-environment.
```python
pipenv shell
```

* To install the dependencies in virtual-environment.
```python
pipenv install
```

* Start server
```python
python manage.py runserver
```

* If you are creating the db for the first time
    - To create database
    ```python
    python manage.py migrate
    ```
    - Run this once to create a superuser for admin panel access
    ```python
    python manage.py createsuperuser
    ```
