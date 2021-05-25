# <p align='center'>*Hello wanderer* :raised_hands:</p>
##### <p align='center'>_We are here with one goal, to make this app the envy of the_</p>
# <p align='center'> `PROS!`:muscle:</p>
Let`s make it step by step...:feet:
***
### 1. Create a virtual environment :flushed:
`python3 -m venv env`

### 2. Activate virtual environment :frowning:
`source env/bin/activate`<br>
`env\Scripts\activate` - on Windows use<br>

### 3. Install the required libraries :books:
`pip install -r requirements.txt`

### 4. Create file ".env" in "ticket_locator": :eyes:
`look at "ticket_locator/.env.example" file`

### 5. Create your local DB migration: :floppy_disk:
`python manage.py migrate`

### 6. Create super user: :shipit:
`python manage.py createsuperuser`

### 7. Run server: 🏃
`python manage.py runserver`

***
# <p align="center">:boom: :boom: :boom: :boom: :boom: `NICE WORK!!!` :boom: :boom: :boom: :boom: :boom:</p>
***

### To go to the admin panel, follow the link in the browser
:point_right:`http://127.0.0.1:8000/admin`

### To work with api use the following links
:point_right:`http://127.0.0.1:8000/api/users` - List of users<br>
:point_right:`http://127.0.0.1:8000/api/users/<user_id>` - User detail view<br>
:point_right:`http://127.0.0.1:8000/api/history` - Search history list<br>
:point_right:`http://127.0.0.1:8000/api/history/<user_id>` - Search history for a specific user<br>
:point_right:`http://127.0.0.1:8000/api/search` - Search flights<br>

### To api test and take api documentations use the following links
:point_right:`http://127.0.0.1:8000/swagger/` - Test Ticket locator api<br>
:point_right:`http://127.0.0.1:8000/redoc/` - Take api documentations<br>
***
### <p align="center">For deploying development area in docker containers:</p>
### 1. Build Docker containers using docker-compose:
`command - sudo docker-compose -f docker-compose_dev.yml build`<br>
`docker-compose -f docker-compose_dev.yml build` - on Windows use<br>
### 2. Start Docker containers using docker-compose:
`command - sudo docker-compose -f docker-compose_dev.yml up`<br>
`docker-compose -f docker-compose_dev.yml up` - on Windows use<br>
***
# <p align="center">May the force be with you. :pray:</p>
