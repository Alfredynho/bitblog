

import yaml


# ~$ PATH - CONFIGURATION
# ---------------------------------------------------------------------

CREDENTIALS_FILE = "credentials.yml"
SERVERS_FILE = "servers.yml"

DB_MYSQL = "mysql"
DB_POSTGRESQL = "postgresql"
DB_SQLITE = "sqlite"

try:
    cfile = open("./config/%s" % CREDENTIALS_FILE, 'r')
    CREDENTIALS = yaml.load(cfile)

    sfile = open("./config/%s" % SERVERS_FILE, 'r')
    SERVERS = yaml.load(sfile)

except Exception as e:
    raise


def get_user_home(stage="develop"):
    return "%(home_path)s/%(user)s" % {
        "home_path": SERVERS[stage]["home_path"],
        "user": SERVERS[stage]["user"],
    }


def get_project_path(stage="develop"):
    return "%(user_home)s/%(project)s" % {
        "user_home": get_user_home(stage),
        "project": SERVERS[stage]["project"],
    }



