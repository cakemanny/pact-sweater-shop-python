# Hatter

This hatter has gone a bit paranoid, they're keeping track of all them orders
and 're makin' all customers prove who they are!

Here we're gonna have an API with a lil' database and some authentication
so that we can work out how we can approach that challenge with pact

## Dev Stuff

### Settings up

First you need virtual environment. My favourite method
```shell
make .venv
echo ". .venv/bin/activate" > .envrc
direnv allow
```

Then installing everything is as simple as
```shell
make install
```
That'll also give you the testing and dev tools in your venv.

### Running tests
Then it's good idea to check you can run the tests and linter
```
make test
make lint
```


### Updating Requirements

Dependencies should be updated in `requirements.in` or `requirements-test.in`
if they are test requirements.
Then recompile the txt files. ([`pip-tools`](https://github.com/jazzband/pip-tools)
should have been installed during `make install`)

```shell
make pip-compile
```


### Running
This ones a django project, so first you wanna
```shell
python manage.py migrate
python manage.py runserver 0:8083
```


## Useful links
- [Django docs](https://docs.djangoproject.com/en/4.2/)
- [Django Rest Framework docs](https://www.django-rest-framework.org/)
