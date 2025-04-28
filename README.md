# BE_Grabber  
### Mini front
python3 serve_frontend.py

### Test html server in local ###
python3 -m http.server 5173 --bind 127.0.0.1

### Run dev: 
 _python grabber/manage.py makemigrations && python grabber/manage.py migrate && hypercorn grabber/grabber.asgi:application --config 
config/hypercorn.dev.toml_  or with _--reload_

Old:
_hypercorn grabber/grabber.asgi:application --config config/hypercorn.dev.toml --reload_

### Run prod:
_python grabber/manage.py makemigrations && python grabber/manage.py migrate && hypercorn grabber/grabber.asgi:application --config 
config/hypercorn.prod.toml_     

Old:
_hypercorn grabber/grabber.asgi:application --config config/hypercorn.prod.toml_




