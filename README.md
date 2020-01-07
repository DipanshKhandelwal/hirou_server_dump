# hirou
Route collection system for Field Protect

## About API server
* This is the server for the `route collection system`.
* It provides interface `API` for connecting web app or mobile app with the database.

## Database
* Database presently used for developemnt is `db.sqlite3`, though it can be replaced by any `sql` server fit for the use like `postgresql`.

## Languages supported
* The project supports two languages for server
    - English : `http://127.0.0.1:8000/en/admin/`
    - Japanese : `http://127.0.0.1:8000/admin/`

## Project structure
* Base project settings : `hirou_server`
* Contains two apps :
    - collection : `collection`
    - users : `users`

* `hirou_server`
    - `settings.py` : It mostly contains the project settings
    - `urls.py` : Has base urls which forwards the request to correct location / views to handle the request

* `collection` and `users`
    - `models.py`: Explains the structure of the data models stored in the database and their details.
    - `admin.py`: Keeps the configurations of the app in the perspective of the admin panel.
    - `serializers.py`: Keeps the configuration of how the API serialization is srtuctured and handled.
    - `urls.py`: Keeps the url endpoints and map it to its view to handle.
    - `views.py`: Explains how the url requests should be handled and ( in case of API ) which serializer to use for handling the request and generating the response.

## Data models
* `collection` models
    - `Vehicle` ( data related to vehicles )
        + `location` : `LocationField` ( present location )
        + `registration number` : `CharField` ( unique, vehicle unique identification number ) 
        + `model` : `CharField` ( store vehicle company model type )
        + `users` : `ManyToManyField` : `Users` ( which users are presently using the vehicle )
    
    - `Item` ( deatils of the item type picked up during the service ) ( Example : `glass`, `paper` )
        + `name` : `CharField` ( unique )
        + `description` : `CharField` ( some description if needed for the items )
    
    - `Area` ( a city is divided into various area, and different areas are assigned to different vehicles )
        + `name` : `CharField` ( unique )
        + `description` : `CharField` ( some description if needed for the area )
    
    - `CollectionPoint` ( different collection points present in the city for grabage pickup )
        + `location` : `LocationField` ( geolocation of the collection point )
        + `name` : `CharField` ( some name  )
        + `address`: `CharField` ( address in plain language )
        + `area` : `ForeignKey` : `Area` ( area the collection point belongs to )

    - `Pickup` ( to store details of the pickup )
        + `collection point` : `ForeignKey` : `CollectionPoint` ( points to which collection point this pickpup happenned )
        + `vehicle` : `ForeignKey` : `Vehicle` ( which vehicle was involved in the pickuip )
        + `timestamp` : `DateTimeField` ( keep track of vehicle and see when the pickup was made )
        + `items`: `ManyToManyField` ( to know which items were picked up during the pickup )
    
* `users` models
    - `Profile` ( data related to users/drivers )
        + `phone_numbers` : `CharField` ( phone number of the drivers )
        + `user`: `OneToOneField` : `DjangoUserModel` ( to keep information regarding the user for `authentication`, `tokens` handling, `sessions` handling, `user blocking` etc )
        + `gender` : `CharField` ( Male / Female )
        + `date_of_birth` : `DateTimeField` ( for age of the driver )
        + `bio` : `CharField` ( to store some details related to driver like `address`, past hostory, `id` etc )
        + `image` : `FileField` ( Storing image of the driver )


## Setup project

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
