.PHONY: requirements
.SILENT: deps static clear_thumbs tests coverage

SETTINGS=settings.local
PYTHON_ENV := DJANGO_SETTINGS_MODULE=$(SETTINGS) ./env/bin/python
COVERAGE_ENV := DJANGO_SETTINGS_MODULE=$(SETTINGS) ./env/bin/coverage
DEPS := grep -vE '^\s*\#' $(CURDIR)/requirements/system.txt  | tr '\n' ' '

help:
	@echo
	@echo ----------------------------------------------------------------------
	@echo "   OWL Build automation file                                        "
	@echo ----------------------------------------------------------------------
	@echo
	@echo "   - install     SETTINGS=[settings]    Install App and their dependencies"
	@echo "   - superuser   SETTINGS=[settings]    Create a super user in production"
	@echo "   - server      SETTINGS=[settings]    Serve project for development"
	@echo "   - mail_server SETTINGS=[settings]    Open the Development Mail Server"
	@echo "   - shell       SETTINGS=[settings]    Run Django in shell mode for development"
	@echo "   - test        SETTINGS=[settings]    Run Django test cases"
	@echo
	@echo ----------------------------------------------------------------------

# COMPOSABLE TASKS
# ------------------------------------------------------------------------------

clear_thumbs:
#	$(PYTHON_ENV) app/manage.py thumbnail clear

db:
	$(PYTHON_ENV) app/manage.py makemigrations
	$(PYTHON_ENV) app/manage.py migrate
	@echo "Migrations in $(SETTINGS) applied..."

load_data:
	$(PYTHON_ENV) app/manage.py load_initial_data
	@echo "Initial data loaded..."

dump_data:
	$(PYTHON_ENV) app/manage.py dumpdata --indent 4 > all.json
	@echo "Fixtures exported"

env:
	virtualenv -p python3 env

deps:
	$(info - Installing all system dependencies using apt-get)
	$(DEPS) | xargs sudo apt-get --no-upgrade install -y --force-yes

requirements:
ifeq ($(SETTINGS),settings.local)
	./env/bin/pip install -r requirements/local.txt
else
	./env/bin/pip install -r requirements/production.txt
endif

static:
ifneq ($(SETTINGS),settings.local)
	@echo "Collect static start..."
	mkdir -p public/static
	mkdir -p public/media

	$(PYTHON_ENV) app/manage.py collectstatic \
	    -v 0 \
	    --noinput \
	    --traceback \
	    -i django_extensions \
	    -i '*.coffee' \
	    -i '*.rb' \
	    -i '*.scss' \
	    -i '*.less' \
	    -i '*.sass'
endif

var:
ifneq ($(SETTINGS),settings.local)
	mkdir -p var/cache
	mkdir -p var/log
	mkdir -p var/db
	mkdir -p var/run
	mkdir -p var/bin
else
	mkdir -p cache
endif

clean_cache:
ifneq ($(SETTINGS),settings.local)
	rm -rf var/cache/*
	rm -rf public/media/cache/*
else
	rm -rf cache/*
endif


# COMMANDS
# ------------------------------------------------------------------------------
install: env requirements var db static clean_cache clear_thumbs

reload: env requirements var db static clean_cache clear_thumbs

superuser:
	$(PYTHON_ENV) app/manage.py createsuperuser

diffsettings:
	$(PYTHON_ENV) app/manage.py diffsettings

shell:
	$(PYTHON_ENV) app/manage.py shell_plus

server:
	@echo "Open your browser at [YOUR_IP]:8000"
	$(PYTHON_ENV) app/manage.py runserver 0.0.0.0:8000

mailserver:
	./tools/mailhog &
	@echo "MailHog opened ..."


tests:
	@echo "Run TestCases [YOUR_IP]:8000"
	rm -rf coverage.svg
	$(COVERAGE_ENV) run app/manage.py test oauth -v 2
	$(COVERAGE_ENV) run app/manage.py test users -v 2
	$(COVERAGE_ENV) report
	$(COVERAGE_ENV)-badge -o coverage.svg

coverage: tests
	$(COVERAGE_ENV) html
	cd coverage &&	../env/bin/python -m http.server  7500

serve_docs:
	cd docs && mkdocs serve --dev-addr=0.0.0.0:8100 --livereload

build_docs:
	cd docs && mkdocs build --clean

