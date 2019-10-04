# A Deadlines app

This is a small Django project to register and manage academic Deadlines
Here are the current django apps that compose this project
- tasks (related to tasks creation and mangement)
- theme (not in use anymore, can be deleted)
- users (related to the Student that signup to use this app)


## Install Required Packages

This project requires a few packages. To install them use the following command:

    pip install -r requirements.txt



## Running the Application

Before running the application we need to create the needed DB tables:

    ./manage.py migrate

Now you can run the development web server:

    ./manage.py runserver

## Running Tests

To run tests on the application:

    ./manage.py test

To access the applications go to the URL <http://localhost:8000/>
