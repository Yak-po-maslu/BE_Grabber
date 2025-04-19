# BE_Grabber


python grabber/manage.py makemigrations && python grabber/manage.py migrate && hypercorn grabber/grabber.asgi:application --config config/hypercorn.dev.toml --reload

### Run dev: 
_hypercorn grabber/grabber.asgi:application --config config/hypercorn.dev.toml --reload_

### Run prod:
_hypercorn grabber/grabber.asgi:application --config config/hypercorn.prod.toml_




