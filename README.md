# BeTale
BeTale is a blog website application base on Django.

### Preparation

You may need Pipenv to create a virtual enviroment:

```
pip install pipenv
```

Clone this repo, and installing dependency packages:

```
git clone https://github.com/sheffeyG/BeTale.git
cd BeTale
pipenv install --dev
```

Run the following command in the project root directory to migrate the database:

```
pipenv run python manage.py migrate
```

Create a backend administrator account by running the following command in the project root

```
pipenv run python manage.py createsuperuser
```

### Running the development server

Run the following command in the project root directory to open the development server:

```
pipenv run python manage.py runserver
```

Visit http://127.0.0.1:8000/admin and log in to the backend to post articles using your administrator account.

Or execute the fake script to generate test data in bulk:

```
pipenv run python -m scripts.fake
```

The batch script will clear all existing data, including the backend administrator account created in step 4. The script will then generate an administrator account by default, with the username and password admin.
