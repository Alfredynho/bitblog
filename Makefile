.PHONY: requirements
.SILENT: deps env static clear_thumbs tests coverage

SETTINGS=config.settings.local
PYTHON_ENV := DJANGO_SETTINGS_MODULE=$(SETTINGS) ./env/bin/python
PIP_ENV := DJANGO_SETTINGS_MODULE=$(SETTINGS) ./env/bin/pip
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


# COMPOSABLE COMMANDS
# ------------------------------------------------------------------------------

clear_thumbs:
#	$(PYTHON_ENV) manage.py thumbnail clear

migrations:
	$(PYTHON_ENV) manage.py migrate
	@echo "Migrations in $(SETTINGS) applied..."

load_data:
	$(PYTHON_ENV) manage.py load_initial_data
	@echo "Initial data loaded..."

load_corpus:
	$(PYTHON_ENV) -m textblob.download_corpora
	@echo "Corpus loaded..."

dump_data:
	$(PYTHON_ENV) manage.py dumpdata --indent 4 > all.json
	@echo "Fixtures exported"

env:
	virtualenv -p python3 env --always-copy --no-site-packages

pip:
	$(PIP_ENV) install pip --upgrade
	$(PIP_ENV) install setuptools --upgrade

requirements:
ifeq ($(SETTINGS),config.settings.local)
	$(PIP_ENV) install -r requirements/local.txt
else
	$(PIP_ENV) install -r requirements/production.txt
endif

static:
ifeq ($(SETTINGS),config.settings.production)
	@echo "Collect static start..."
	mkdir -p public/static
	mkdir -p public/media

	$(PYTHON_ENV) manage.py collectstatic \
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
	mkdir -p var/cache
	mkdir -p var/log
	mkdir -p var/db
	mkdir -p var/run
	mkdir -p var/bin

clean_cache:
ifneq ($(SETTINGS),config.settings.local)
	rm -rf var/cache/*
	rm -rf public/media/cache/*
else
	rm -rf cache/*
endif


# DEV COMMANDS
# ------------------------------------------------------------------------------
mailserver:
	./tools/bin/mailhog &
	@echo "MailHog opened ..."

deps:
	$(info - Installing all system dependencies using apt-get)
	sudo ./tools/scripts/system.sh install

database:
	sudo ./tools/scripts/database.sh reset
	@echo "---"
	@echo "Database has been reseted"



# BOTH COMMANDS
# ------------------------------------------------------------------------------
install: env requirements var migrations static clean_cache clear_thumbs

reload: env requirements var migrations static clean_cache clear_thumbs

superuser:
	$(PYTHON_ENV) manage.py createsuperuser

corpora:
	$(PYTHON_ENV) -m textblob.download_corpora

diffsettings:
	$(PYTHON_ENV) manage.py diffsettings

shell:
	$(PYTHON_ENV) manage.py shell_plus

server:
	@echo "Open your browser at [YOUR_IP]:8000"
	$(PYTHON_ENV) manage.py runserver 0.0.0.0:8000

tunnel:
	@echo "Open a tunnel to [YOUR_IP]:8000"
	./ngrok http 8000

tests:
	@echo "Run TestCases [YOUR_IP]:8000"
	#rm -rf coverage.svg
	$(COVERAGE_ENV) run manage.py test apps.credentials -v 2
	#$(COVERAGE_ENV) run manage.py test users -v 2
	#$(COVERAGE_ENV) report
	#$(COVERAGE_ENV)-badge -o coverage.svg

coverage: tests
	$(COVERAGE_ENV) html
	cd coverage &&	../env/bin/python -m http.server  7500

docs:
	cd docs && mkdocs serve --dev-addr=0.0.0.0:8100 --livereload

build_docs:
	cd docs && mkdocs build --clean
