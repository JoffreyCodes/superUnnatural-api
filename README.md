This app consist of backend features that make calls to the Supernatural api and renders a parsed out JSON for front-end development.
Build Dockerfile into image
`docker image build -t docker-superunnatural-api .`
Run the image into a container
`docker run --rm -p 80:5000 docker-superunnatural-api`
