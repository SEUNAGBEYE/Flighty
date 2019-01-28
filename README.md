## Flighty

A flight booking app to automate processes around booking flights.


## Key Application features

- Log in
- Upload passport photographs
- Book tickets
- Receive tickets as an email
- Check the status of their flight
- Make flight reservations
- Purchase tickets (you can add a payment gateway. Since it won't be used live you can always use a dummy card)
 
 

The flight booking system should be able to:

encrypt password
handle multiple requests
optimize via caching and multithreading

### API Documentation
```
Coming Soon!
```

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
    ```
-   Check that postgres is installed:

    ```
    postgres --version
    >> postgres (PostgreSQL) 10.1
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


-   Activate a virtual environment:

    ```
    pipenv shell
    ```



-   Run the application:

    ```
    cd flighty
    python manage.py runserver
    >>> Django version 2.1.5, using settings 'flighty.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    ```



-   Deactivate the virtual environment once you're done:
    ```
    exit
    ```

## Contribution guide

##### Contributing

All proposals for contribution must satisfy the guidelines in the product wiki.
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.This Project shall be utilising a [Pivotal Tracker board](https://www.pivotaltracker.com/n/projects/2170023) to track the work done.

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
