## Warp - Backend


An Awesome Django Backend Template

### Technologies

  * [Django](https://www.djangoproject.com/)
  * [Django Rest Framework](http://www.django-rest-framework.org/)
  * [Compass](http://compass-style.org/)
  * [Semantic UI](http://semantic-ui.com/)

## Features
  * `cd project/`

### Installation

#### Linux

  * `cd project/`
  * `make install`
  * `make superuser`
  * `make server`
  * To know more dev commands type: `make help`


##### MacOS, Windows

  * `vagrant up`
  * `vagrant ssh` choose a network and type you password if is necesary.
  * `cd code/`
  * Execute linux commands after here

### Deployment
For deployment you need this tools:

  * fabric  `[sudo] pip install fabric`
  * PyYaml  `[sudo] pip install pyyaml`
  * To know deployment commands type:  `fab help`

### TODOS
  - Add fabric tasks to use `letsencrypt` and enhace nginx template to support it
  - Implement docker configuration.
  - Implement docker-compose to development and production environments.
  - Upload and docker image to dockerhub.


### Commercial Support

Warpp is supported by [@jvacx](http://jvacx.com).
If you need help implementing or deployment, please contact us: **victor@jvacx.com.**
