# UberooApiGateway

### Author
__Nikita ROUSSEAU__
### Updated
__00:00 30/10/2018__

## Requirements

- Python 3.6.x
- Dependencies :
  * flask
  * kafka-python

### Install Dependencies

```bash
pip install --trusted-host pypi.python.org -r requirements.txt
```

## Deployment

You can start the server in (`development`|`production`) environment. Set `FLASK_ENV` according to your needs.

```bash
export FLASK_APP=app.py
export FLASK_ENV=development

flask run --host 0.0.0.0 --port 5000

# * Serving Flask application
```

## Docker

### Build
`docker build -t uberooapigateway .`

### Run
`docker run -p 5000:5000 uberooapigateway`

### Publish
```bash
mint-virtual-machine # docker login --username=nrousseauetu
Password: 
Login Succeeded
mint-virtual-machine # docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
uberooapigateway    latest              dea9321cc24c        7 minutes ago       155MB
python              3.6.5-slim          b31cb11e68a1        3 months ago        138MB
mint-virtual-machine SI5_soa_api_lab_team_d_menu_service # docker tag dea9321cc24c uberoolab/team-d-apigateway:latest
mint-virtual-machine SI5_soa_api_lab_team_d_menu_service # docker push uberoolab/team-d-apigateway
The push refers to repository [docker.io/uberoolab/team-d-apigateway]
[...]
```

### Pull From Hub
`docker pull uberoolab/team-d-apigateway`

### Run From Hub (Interactive)
`docker run -i -p 5000:5000 -t uberoolab/team-d-apigateway`

### Run From Hub (Detached)
`docker run -d -p 5000:5000 -t uberoolab/team-d-apigateway`

## Api Documentation

// TODO