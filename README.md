## BitBlog

BitBlog is a blog app for django, it is developed with wagtail and focused to 
tech bloggers, It was created for the blog [victoraguilar.net](http://victoraguilar.net/).


### Technologies

  * [Django](https://www.djangoproject.com/)
  * [Django Rest Framework](http://www.django-rest-framework.org/)
  * [Compass](http://compass-style.org/)

## Functionalities
  * Usuario, Authenticación
  * Servicios web para aplicaciones


##### Development

  * `docker-compose -f dev.yml build` Build project images.
  * `docker-compose -f dev.yml up` Up images.
  * `export COMPOSE_FILE=dev.yml` Exports `dev.yml` as default config file. 
  * `docker-compose up` up images.
  * `docker-compose run django python manage.py migrate` Run migrations.
  * `docker-compose run django python manage.py createsuperuser` Create superusers.

  * `brew install socat` Socket utilitie for MacOS to configure pycharm.
  * `socat -d -d TCP-L:8099,fork UNIX:/var/run/docker.sock` trunk a file socke as port socket number `8099`.
  * Configure pycharm and add API URL as: `tcp://localhost:8099` without certificates.


### Commercial Support

BitBlog is supported by [@vicobits](http://victoraguilar.net) and [@xiberty](http://xiberty.com) team.
for any questions tell to **hello@victoraguilar.net.**
