## Flighty

[![Coverage Status](https://coveralls.io/repos/github/SEUNAGBEYE/Flighty/badge.svg?branch=develop)](https://coveralls.io/github/SEUNAGBEYE/Flighty?branch=develop)

A flight booking app to automate processes around booking flights.


## Key Application features

- Log in
- Upload passport photographs
- Book tickets
- Receive e-tickets as an email
- Check the status of their flight
- Make flight reservations
- Purchase tickets
 
## Technologies Used

- DRF (API)
- RabbitMQ (Message Broker)
- Celery (Tasks Management)
- POSTMAN (API Documentation)


### API Documentation

[Flighty](https://documenter.getpostman.com/view/2969248/RztrHmL7)

### Development set up

-   Check that python 3 is installed:

    ```
    python --v
    >> Python 3.6.5
    ```

-   Install pipenv:

    ```
    brew install pipenv (Mac)
    pip install pipenv (Windows | Unix)
    
    You might get the error below if you are on a Windows system. Worry not, all you need to do is follow this [instruction](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip) to install pip
    >> pip not found
    ```

-   Check pipenv is installed:
    ```
    pipenv --version
    >> pipenv, version 2018.6.25

    Please install pipenv if not installed
    ```


-   Clone the flighty repo and cd into it:

    ```
    git clone git@github.com:SEUNAGBEYE/Flighty.git
    ```

-   Install dependencies:

    ```
    pipenv install
    ```

-   Install dev dependencies to setup development environment:

    ```
    pipenv install --dev
    ```
  
- Create a `.env` file


  create a .env file and populate the the following env variable
```
SECRET_KEY=<JWT-SECRET-KEY>
DJANGO_ENV=<YOUR ENVIRONMENT> This should be set to development
EMAIL_HOST_USER = <email address for sending notification> gmail,yahoo, e.t.c
EMAIL_HOST_PASSWORD = <password for the above email address>
```


-   Activate a virtual environment:

    ```
    pipenv shell
    ```



-   Run the application:

    ```
    python manage.py runserver
    >>> Django version 2.1.5, using settings 'flighty.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    ```

- Run Celery
  ```
    celery -A flighty worker --loglevel=debug
  ```

- Run Celery Beat
  ```
  celery -A flighty beat -l INFO
  ```

- Run RabbitMQ
  ```
  rabbitmq-server

  export PATH=$PATH:/usr/local/sbin
  ```

-   Deactivate the virtual environment once you're done:
    ```
    exit
    ```

- Run Test
```
coverage run --source='.' manage.py test user
```

- Generate html report
```
coverage html
```

## Contribution guide

##### Contributing

All proposals for contribution must satisfy the guidelines in the product wiki.
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.This Project shall be utilising a [Pivotal Tracker board](https://www.pivotaltracker.com/n/projects/2237877) to track the work done.

##### Pull Request Process

-   A contributor shall identify a task to be done from the [pivotal tracker](https://www.pivotaltracker.com/n/projects/2170023).If there is a bug , feature or chore that has not been included among the tasks, the contributor can add it only after consulting the owner of this repository and the task being accepted.
-   The Contributor shall then create a branch off the `develop` branch where they are expected to undertake the task they have chosen.
-   Contributors are required to activate the git pre-commit hook to auto format staged Python files to pep8 with yapf and check for residual pep8 linting errors using pylint.
    All commits are required to pass all checks from the pre-commit hook.
    The pre-commit hook can be installed as follows:
    Option 1: Copy the `hooks/pre-commit` file into the `.git/hooks` directory.
    You will need to do this every time the `hooks/pre-commit` file is changed.
    Option 2: Create a file `.git/hooks/pre-commit` then create a symlink to this file by running the command:
    `ln -s -f ../../hooks/pre-commit .git/hooks/pre-commit`
    You will only need to do this once for your local repository.
-   Although highly discouraged, the pre-commit hook can be bypassed by passing the `--no-verify` flag to the commit command as follows:
    `git commit --no-verify -m "commit message"`
-   After undertaking the task, a fully detailed pull request shall be submitted to the owners of this repository for review.
-   If there any changes requested ,it is expected that these changes shall be effected and the pull request resubmitted for review.Once all the changes are accepted, the pull request shall be closed and the changes merged into `develop` by the owners of this repository.
