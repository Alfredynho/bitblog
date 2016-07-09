from __future__ import unicode_literals
from fabric.api import *
from fabric.contrib.files import exists, upload_template

from tasks.config import *


class Server(object):
    @staticmethod
    def upgrade():
        """
        Update and upgrade server.
        """
        sudo('apt-get update -y')
        sudo('apt-get upgrade -y')

    @staticmethod
    def deps():
        """
        Install all server dependencies.
        """
        sudo('apt-get install -y %s' % env.pkgs)

    @staticmethod
    def restart_services():
        """
        1. Update Supervisor configuration if app supervisor config exist.
        2. Restart nginx.
        3. Restart supervisor.
                """
        if exists('%s/var/log' % get_project_path(env.stage)):
            sudo('supervisorctl reread')
            sudo('supervisorctl update')

        sudo('service nginx restart')
        sudo('service supervisor restart')
        sudo('supervisorctl restart %s' % env.project)

    @staticmethod
    def configure_locales():
        """
        Generate and configure locales in recently installed server.
        """
        sudo("locale-gen en_US.UTF-8")
        sudo("dpkg-reconfigure locales")

    @staticmethod
    def nginx():
        """
        1. Remove default nginx config file
        2. Create new config file
        3. Copy local config to remote config
        4. Setup new symbolic link
        """
        # nginx remove default config
        if exists('/etc/nginx/sites-enabled/default'):
            sudo('rm /etc/nginx/sites-enabled/default')

        # nginx config domain file
        if exists('/etc/nginx/sites-enabled/%s' % env.domain):
            sudo('rm /etc/nginx/sites-enabled/%s' % env.domain)
        if exists('/etc/nginx/sites-available/%s' % env.domain):
            sudo('rm /etc/nginx/sites-available/%s' % env.domain)

        # Main domain configuration
        with lcd("./config/tmpl"):
            with cd('/etc/nginx/sites-available/'):
                upload_template(
                    filename="./nginx.conf",
                    destination='/etc/nginx/sites-available/%s' % env.domain,
                    template_dir="./",
                    context={
                        "project_name": env.project,
                        "project_path": get_project_path(env.stage),
                        "project_url": env.urls,
                    },
                    use_sudo=True,
                )

        sudo('ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled/' % env.domain)

        # nginx config docs domain file
        if exists('/etc/nginx/sites-enabled/docs.%s' % env.domain):
            sudo('rm /etc/nginx/sites-enabled/docs.%s' % env.domain)
        if exists('/etc/nginx/sites-available/docs.%s' % env.domain):
            sudo('rm /etc/nginx/sites-available/docs.%s' % env.domain)

        # Docs domain configuration
        with lcd("./config/tmpl"):
            with cd('/etc/nginx/sites-available/'):
                upload_template(
                    filename="./docs.conf",
                    destination='/etc/nginx/sites-available/docs.%s' % env.domain,
                    template_dir="./",
                    context={
                        "project_name": env.project,
                        "project_path": get_project_path(env.stage),
                        "project_url": env.docs,
                    },
                    use_sudo=True,
                )

        sudo('ln -s /etc/nginx/sites-available/docs.%s /etc/nginx/sites-enabled/' % env.domain)

    @staticmethod
    def gunicorn():
        """
        1. Create new gunicorn start script
        2. Copy local start script template redered to server
        """

        sudo('rm -rf %s/bin' % get_project_path(env.stage))
        sudo('mkdir -p %s/bin' % get_project_path(env.stage))

        with lcd("./config/bin"):
            with cd('%s/bin' % get_project_path(env.stage)):
                upload_template(
                    filename='./start.sh',
                    destination='%s/bin/start.sh' % get_project_path(env.stage),
                    template_dir="./",
                    context={
                        "project_name": env.project,
                        "project_path": get_project_path(env.stage),
                        "app_user": SERVERS[env.stage]["user"],
                        "app_group": SERVERS[env.stage]["team"],
                    },
                    use_sudo=True,
                )
                sudo('chmod +x %s/bin/start.sh' % get_project_path(env.stage))

    @staticmethod
    def supervisor():
        """
        1. Create new supervisor config file.
        2. Copy local config to remote config.
        3. Register new command.
        """
        if exists('/etc/supervisor/conf.d/%s.conf' % env.domain):
            sudo('rm /etc/supervisor/conf.d/%s.conf' % env.domain)

        with lcd("./config/tmpl"):
            with cd('/etc/supervisor/conf.d'):
                upload_template(
                    filename="./supervisor.conf",
                    destination='./%s.conf' % env.domain,
                    template_dir="./",
                    context={
                        "project_name": env.project,
                        "project_path": get_project_path(env.stage),
                        "app_user": SERVERS[env.stage]["user"],
                    },
                    use_sudo=True,
                )

    @staticmethod
    def git():
        """
        1. Setup bare Git repo.
        2. Create post-receive hook.
        """
        if exists(env.home_path) is False:
            sudo('mkdir %s' % env.home_path)

        if exists(get_user_home(env.stage)) is False:
            sudo("mkdir %s" % get_user_home(env.stage))

        if exists(get_project_path(env.stage)) is False:
            sudo("mkdir %s" % get_project_path(env.stage))

        with cd(get_user_home(env.stage)):
            sudo('mkdir -p %s.git' % env.project)
            with cd('%s.git' % env.project):
                sudo('git init --bare')
                with lcd("./config/bin"):
                    with cd('hooks'):
                        upload_template(
                            filename="post-receive",
                            destination=get_project_path(env.stage)+".git/hooks",
                            template_dir="./",
                            context={
                                "project_path": get_project_path(env.stage),
                            },
                            use_sudo=True,
                        )
                        sudo('chmod +x post-receive')

            sudo('chown -R %(user)s:%(team)s %(project)s.git' % {
                "user": SERVERS[env.stage]["user"],
                "team": env.team,
                "project": env.project,
            })

    @staticmethod
    def add_remote():
        """
        1. Delete existent server remote git value.
        2. Add existent server remote git value.
        """
        local('git remote remove %s' % env.stage)
        local('git remote add %(remote_name)s %(user)s@%(ip_address)s:%(user_home)s/%(project)s.git' % {
            "remote_name": env.stage,
            "user": SERVERS[env.stage]["user"],
            "ip_address": SERVERS[env.stage]["ip_address"],
            "user_home": get_user_home(env.stage),
            "project": env.project,
        })

    @staticmethod
    def user():
        """
         Create app user.
        """
        sudo('adduser %(user)s --home %(home_path)s/%(user)s --disabled-password --gecos \"\"' % {
            "user": SERVERS[env.stage]["user"],
            "home_path": env.home_path,
        })

        sudo('echo \"%(user)s:%(password)s\" | sudo chpasswd' % {
            "user": SERVERS[env.stage]["user"],
            "password": SERVERS[env.stage]["password"],
        })

        sudo('mkdir -p %s' % get_user_home(env.stage))

    @staticmethod
    def group():
        """
         Create app group.
        """
        sudo('groupadd --system %s' % env.team)
        sudo('useradd --system --gid %(team)s \
              --shell /bin/bash --home %(user_home)s %(user)s' % {
            "team": env.team,
            "user_home": get_user_home(env.stage),
            "user": SERVERS[env.stage]["user"],
        })

    @staticmethod
    def fix_permissions():
        """
         Fix Permissions.
        """
        sudo('chown -R %(user)s %(user_home)s' % {
            "user": SERVERS[env.stage]["user"],
            "user_home": get_user_home(env.stage),
        })

        sudo('chown -R %(user)s:%(team)s %(project_path)s' % {
            "user": SERVERS[env.stage]["user"],
            "team": env.team,
            "project_path": get_project_path(env.stage),
        })

        sudo('chmod -R g+w %s' % get_project_path(env.stage))

    @staticmethod
    def postgresql():
        """
        1. Create DB user.
        2. Create DB and assign to user.
        """
        sudo('psql -c "CREATE USER %(db_user)s WITH NOCREATEDB NOCREATEUSER \
            ENCRYPTED PASSWORD E\'%(db_pass)s\'"' % {
                "db_user": SERVERS[env.stage]["user"],
                "db_pass": SERVERS[env.stage]["password"],
            }, user='postgres')

        sudo('psql -c "CREATE DATABASE %(db_name)s WITH OWNER %(db_user)s"' % {
                "db_name": env.project,
                "db_user": SERVERS[env.stage]["user"],
            }, user='postgres')

    @staticmethod
    def mysql():
        """
        1. Verify id user exist.
        2. If not user exist create DB user.
        3. Verify if database exist.
        4. If DB not exist create DB and assign to user.
        """

        # CREATE DATABASE
        run("mysql -u %(mysql_user)s -p%(mysql_password)s -e 'CREATE DATABASE %(database)s;'" % {
            "mysql_user": CREDENTIALS[env.stage]["mysql_user"],
            "mysql_password": CREDENTIALS[env.stage]["mysql_password"],
            "database": env.project,
        })

        # CREATE USER
        run("mysql -u %(mysql_user)s -p%(mysql_password)s -e "
            "'CREATE USER \"%(user)s\"@\"localhost\" IDENTIFIED BY \"%(password)s\";'" % {
                "mysql_user": CREDENTIALS[env.stage]["mysql_user"],
                "mysql_password": CREDENTIALS[env.stage]["mysql_password"],
                "user": SERVERS[env.stage]["user"],
                "password": SERVERS[env.stage]["password"],
            })

        # GRANT USER TO DB
        run("mysql -u %(mysql_user)s -p%(mysql_password)s -e "
            "'GRANT ALL PRIVILEGES ON %(database)s.* TO \"%(user)s\"@\"localhost\";'" % {
                "mysql_user": CREDENTIALS[env.stage]["mysql_user"],
                "mysql_password": CREDENTIALS[env.stage]["mysql_password"],
                "database": env.project,
                "user": SERVERS[env.stage]["user"],
            })

        run("mysql -u %(mysql_user)s -p%(mysql_password)s -e 'FLUSH PRIVILEGES;'" % {
            "mysql_user": CREDENTIALS[env.stage]["mysql_user"],
            "mysql_password": CREDENTIALS[env.stage]["mysql_password"],
        })

    @staticmethod
    def clean():
        """
        1. kill all user's processes.
        2. Delete app user folder.
        3. Delete project folder.
        4. Delete supervisor and nginx config files.
        5. Drop app and user in database.
        6. Delete app socket.
        7. Delete app group.
        8. Delete app user.
        """
        sudo('pkill -u %s' % SERVERS[env.stage]["user"])

        Server.drop_db()

        if exists(get_project_path(env.stage)):
            sudo('rm -rf %s' % get_project_path(env.stage))

        if exists('/etc/supervisor/conf.d/%s.conf' % env.domain):
            sudo('rm -f /etc/supervisor/conf.d/%s.conf' % env.domain)

        if exists('/etc/nginx/sites-enabled/%s' % env.domain):
            sudo('rm -f /etc/nginx/sites-enabled/%s' % env.domain)

        if exists('/etc/nginx/sites-available/%s' % env.domain):
            sudo('rm -f /etc/nginx/sites-available/%s' % env.domain)

        sudo('rm -rf /tmp/%s.socket' % env.project)
        sudo('groupdel %s' % env.team)
        sudo('userdel -r %s' % SERVERS[env.stage]["user"])
        sudo("rm -rf %s" % get_user_home(env.stage))

    @staticmethod
    def drop_db():
        if SERVERS[env.stage]["enginedb"] == DB_MYSQL:
            run("mysql -u %(mysql_user)s -p%(mysql_password)s -e 'DROP DATABASE %(database)s;'" % {
                "mysql_user": CREDENTIALS[env.stage]["mysql_user"],
                "mysql_password": CREDENTIALS[env.stage]["mysql_password"],
                "database": env.project,
            })

            run("mysql -u %(mysql_user)s -p%(mysql_password)s -e 'DROP USER \"%(user)s\"@\"localhost\";'" % {
                "mysql_user": CREDENTIALS[env.stage]["mysql_user"],
                "mysql_password": CREDENTIALS[env.stage]["mysql_password"],
                "user": SERVERS[env.stage]["user"],
            })

            run("mysql -u %(mysql_user)s -p%(mysql_password)s -e 'FLUSH PRIVILEGES;'" % {
                "mysql_user": CREDENTIALS[env.stage]["mysql_user"],
                "mysql_password": CREDENTIALS[env.stage]["mysql_password"],
            })

        elif SERVERS[env.stage]["enginedb"] == DB_POSTGRESQL:
            sudo('psql -c "DROP DATABASE %s"' % env.project, user='postgres')
            sudo('psql -c "DROP ROLE IF EXISTS %s"' % SERVERS[env.stage]["user"], user='postgres')
        else:
            pass # TODO configure ORACLE or SQLITE3

    @staticmethod
    def create_db():
        if SERVERS[env.stage]["enginedb"] == DB_MYSQL:
            Server.mysql()
        elif SERVERS[env.stage]["enginedb"] == DB_POSTGRESQL:
            Server.postgresql()
        else:
            pass # TODO configure ORACLE or SQLITE3

    @staticmethod
    def reset_db():
        Server.drop_db()
        Server.create_db()

    @staticmethod
    def pip_cache():
        run("printf '[global]\ndownload_cache = ~/.cache/pip\n' > ~/.pip/pip.conf")
        run("mkdir -p ~/.cache/pip")
