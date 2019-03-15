[![Build Status](https://travis-ci.org/Celoka/flight_booking_system.svg?branch=master)](https://travis-ci.org/Celoka/flight_booking_system)
[![Coverage Status](https://coveralls.io/repos/github/Celoka/flight_booking_system/badge.svg?branch=integrate_ci)](https://coveralls.io/github/Celoka/flight_booking_system?branch=integrate_ci)

# Flight Booking System
This repository contains the API endpoints of Airtech Services. This enables users to be authenticated and authorized before booking a flight ticket, purchase tickets, make flight reservations amongst others. This project is built using Django rest framework. 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
- Install `pip` if it is not installed yet in your system

-  To install virtual environment, run in your terminal:
```
pip install virtualenv
```
- To create a virtual environment, in the root folder of the cloned app, run:
```
virtualenv -p python3 venv
```
- To activate the virtualenv:
```
source venv/bin/activate
```

- Run the command below to install all the project dependencies:
```
pip install -r requirements.txt
```
- To deactivate the virtualenv:
```
deactivate
```
### Installing
- Clone this repository
> https://github.com/Celoka/flight_booking_system.git

- Cd into the cloned app, create a virtualenv and activate(see instruction above for steps to create a virtualenv)

- Create a `.env` file, copy the variables in the `.env_sample` in the root directory of the project and set up the configurations according to your system.

- Ensure to create makemigrations then migrate by running the following commands sequencially:
```
- python manage.py makemigrations

- python manage.py migrate
```

- To start the application, in the root directory of the project, run:
```
python manage.py runserver
```

- Run the below command to start Celery worker and Celery beat:
```
celery -A flight_booking_api worker --loglevel=info

celery -A flight_booking_api beat --loglevel=info
```

- To start up the RabbitMQ server:
```
rabbitmq-server
```
## Running the tests

- To run test:
```
python manage.py test
```

- Test coverage:
```
coverage run manager.py
```

- Coverage report:
```
coverage report
```
## Features of the Project
- Registration
- Login
- Upload Passport Photo
- Admin Create Flight
- Book Tickets
- Purchase Tickets
- Receive Tickets as Email
- Make Flight Reservation
- Check Flight Status

## Built With
- Python 3
- Postgresql
- Django Rest Framework (API development)
- Celery (Asynchronous Task Queue)
- RabbitMQ (A message broker)
- Insomnia (API Test tool)

## Authors
- Eloka Chima

## License
- This project is licensed under the MIT License - see the [LICENCE](https://github.com/Celoka/flight_booking_system/blob/master/LICENSE) file for details
