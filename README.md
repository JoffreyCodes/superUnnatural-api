This app consist of backend features that make calls to the Supernatural api and renders a parsed out JSON for front-end development.
Build Dockerfile into image
`docker image build -t docker-superunnatural-api .`
Run the image into a container
`docker run --rm -p 80:5000 docker-superunnatural-api`

Loading the DB

https://stackoverflow.com/questions/51789475/flask-sqlalchemy-load-database-with-records-by-running-python-script
https://flask.palletsprojects.com/en/1.0.x/cli/#custom-commands
