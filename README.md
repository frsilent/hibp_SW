# Have I Been Pwned Interface
## Demonstration application for providing restful APIs & querying them

# Installation

> git clone https://github.com/frsilent/hibp_SW

> cd hibp_SW

> pip install -r requirements.txt

> export LC_ALL=en_US.UTF-8

> export LANG=en_US.UTF-8

> python3 ./app.py

> navigate to 127.0.0.1:5000

# Notes
```
Uses swagger for api documentation; api documentation is derive from route method docstrings via flasgger
```
```
sqlite is used in an effort to get rid of redundant external api calls
```
```
HIBP presently returns an empty 404 if no breaches are found
```
```
http://127.0.0.1:5000/apidocs/#!/default/get_passwords_password is used for human-facing usage & documentation \
but all existing logic could also be wrapped in another view/template; decided against duplicating module's work
```

# Setup

## Procfile can be used to setup heroku instance
> git clone https://github.com/frsilent/hibp_SW
> heroku create
> git push heroku master
> heroku open
