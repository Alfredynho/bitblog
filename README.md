## Warpp Backend

**Warpp** Plataforma Base
### Tecnologías

  * [Django](https://www.djangoproject.com/)
  * [Django Rest Framework](http://www.django-rest-framework.org/)
  * [Less](http://compass-style.org/)
  * [Booya Template](http://semantic-ui.com/)

## Funcionalidades
  * Usuario, Authenticación
  * Servicios web para aplicaciones


##### MacOS, Windows

  * `vagrant up` Inicia la maquina virtual del proyecto.
  * `vagrant ssh` Inicia session en la maquina virtual del proyecto via ssh.
  * `cd code/`
  * A partir de este punto ejecutar los comandos para Linux.

#### Linux

  1. `cd project/`
  2. `sudo apt-get install buil-essential` Instala lo minimo para tener el comando `make` disponible.
  3. Crear los archivos `server.json` para tener la configuración local/producción y `.environment`
     para tener los valores de las variables de entorno para **warpp**.
  4. `make deps` Instala las dependencias del sistema.
  5. `make database` Configura la base de datos en forma local, por el momento solo para `postgresql`.
  6. `make install` Instala las dependencias del proyecto.
  7. `make superuser` Crea un cuper usuario.
  8. `make server` Inicia el servidor.
  9. `make mailserver` Inicia un servidor de correos para desarrollo.
  10. `make help` Muestra la lista de comandos disponibles

##### Desarrollo con Docker/MacOS

  * `docker-compose -f dev.yml build` Construye las imagenes con el proyecto.
  * `docker-compose -f dev.yml up` Crea imagenes a partir de las imagenes construidas y ejecuta el proyecto.
  * `export COMPOSE_FILE=dev.yml` Exporta una variable para tener por defecto `dev.yml` como archivo de configuración. 
  * `docker-compose up` Ejecuta el proyecto.
  * `docker-compose run django python manage.py migrate` Para ejecutar migraciones.
  * `docker-compose run django python manage.py createsuperuser` Para crear un superusuario.
  * `brew install socat` instala socat, una utilidad para tener un socket como puerto y asi configurar pycharm.
  * `socat -d -d TCP-L:8099,fork UNIX:/var/run/docker.sock` Desvia el socker de docker al puerto `8099`.
  * Configurar pycharm, API URL como: `tcp://localhost:8099` sin certificados de seguridad.


### Despliegue
Para el despliegue hara falta tener instalado de forma global las siguientes herramientas.

  * `[sudo] pip install fabric` Gestor de tareas de despliegue.
  * `[sudo] pip install jinja2` Motor de plantillas para los archivos de configuración.
  * `[sudo] pip install python-digitalocean` paquete para configurar droplets en digitalocean.
  * `fab help` Muestra los comando disponibles para el despliegue.

### Solución al error del idioma (Linux).
  * `sudo apt-get install language-pack-es`
  * `sudo locale-gen "es_US.UTF-8"`
  * `sudo dpkg-reconfigure locales`  
  * `echo "export LANG=C.UTF-8" >> ~/.bash_profile`  
  * `echo "export LC_CTYPE=C.UTF-8" >> ~/.bash_profile`  
  * `echo "export LC_ALL=C.UTF-8" >> ~/.bash_profile`

### Tareas.
  - Soportar Docker
  - Estilizar todos los correos de activacion y transacción.

### Commercial Support

Warpp es soportado por [@vicobits](http://victoraguilar.net) y el team [@botmerang](http://botmerang.com).
para posibles dudas contactate a : **hello@victoraguilar.net.**
