#!/bin/bash

APP_NAME=%(project_name)s                              # Application Name

PROJECT_PATH=%(project_path)s                          # Project path
PROJECT_DJANGO=${PROJECT_PATH}/app
PYTHON_ENV=${PROJECT_PATH}/env                           # Virtual environment path

SOCKET_PATH=/tmp                                       # Root socket path
SOCKET_FILE=${SOCKET_PATH}/${APP_NAME}.socket              # Socket file path


USER=%(app_user)s                                      # Application user
GROUP=%(app_group)s
NUM_WORKERS=3                                          # workers CPUs*2+1

DJANGO_SETTINGS_MODULE=settings.production             # Settings to production mode
DJANGO_WSGI_MODULE=wsgi                                # WSGI Module
BIND=unix:$SOCKET_FILE                                 # Socket to binding

echo "Starting $NAME as `whoami`"

cd ${PROJECT_PATH}
source env/bin/activate
cd ${PROJECT_DJANGO}

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
export PYTHONPATH=${PROJECT_DJANGO}:${PYTHONPATH}

# test if exist socket path
test -d ${SOCKET_PATH} || mkdir -p ${SOCKET_PATH}

# Execute django app
# Los programas que se ejecutaran bajo **supervisor** no deben demonizarse a si mismas (no usar --daemon)
exec ${PYTHON_ENV}/bin/gunicorn wsgi:application \
  --name=${APP_NAME} \
  --workers ${NUM_WORKERS} \
  --user=${USER} --group=${GROUP} \
  --bind=${BIND} \
  --log-file=-
  # --log-level=debug \
