from __future__ import unicode_literals
from tasks.utils import *
from tasks.server import *
from tasks.project import *


#TODO Clean APP variables

# ~$ COMMANDS
# ---------------------------------------------------------------------

@task
def external():
    """
    Set stage as production.
    """
    set_stage('external')

@task
def production():
    """
    Set stage as production.
    """
    set_stage('production')


@task
def develop():
    """
    Set stage as develop.
    """
    # TODO Arreglar la creacion de los archivos de log y la creacion de la base de datos en desarrollo.
    set_stage('develop')


@task
def test():
    """
    Set stage as test.
    """
    set_stage('test')


@task
def restart():
    """
    Restart all app services.
    """
    set_user(superuser=True)
    with settings(warn_only=True):
        execute(Server.restart_services, hosts=env.hosts)


@task()
def deploy():
    """
    Deploy application in selected server(s)
    """
    set_user()
    with settings(warn_only=True):
        execute(Project.push, hosts=env.hosts)
        execute(Project.environment, hosts=env.hosts)
        execute(Project.clean_logs, hosts=env.hosts)
        execute(Project.clean_cache, hosts=env.hosts)
        execute(Project.reload, hosts=env.hosts)


@task
def install():
    """
    Install app in selected server(s).
    """
    pkgs = local("grep -vE '^\s*\#' ./requirements/system.txt  | tr '\n' ' '", capture=True)
    env.pkgs = pkgs
    set_user(superuser=True)
    with settings(warn_only=True):
        execute(Server.clean, hosts=env.hosts)
        execute(Server.pip_cache, hosts=env.hosts)
        execute(Server.deps, hosts=env.hosts)
        execute(Server.user, hosts=env.hosts)
        execute(Server.group, hosts=env.hosts)
        execute(Server.create_db, hosts=env.hosts)
        execute(Server.git, hosts=env.hosts)
        execute(Server.add_remote, hosts=env.hosts)
        execute(Server.nginx, hosts=env.hosts)
        execute(Server.gunicorn, hosts=env.hosts)
        execute(Server.supervisor, hosts=env.hosts)
        execute(Server.fix_permissions, hosts=env.hosts)


@task
def uninstall():
    """
    Uninstall app in selected server(s)
    """
    set_user(superuser=True)
    with settings(warn_only=True):
        execute(Server.clean, hosts=env.hosts)


@task
def add_remote():
    """
    Add project repo url to local git configuration.
    """
    with settings(warn_only=True):
        execute(Server.add_remote, hosts=env.hosts)


@task
def upload_key():
    """
    Upload SSH key to server.
    """
    set_user()
    with settings(warn_only=True):
        execute(Utils.upload_key, hosts=env.hosts)


@task
def reset_db():
    """
    Reset the env Database
    """
    reset = prompt("Reset Database, Are you sure? (y/N)", default="N")

    if reset == 'y' or reset == 'Y':
        set_user(superuser=True)
        with settings(warn_only=True):
            execute(Server.reset_db, hosts=env.hosts)


@task
def reset_env():
    """
    Reset the python env
    """
    reset = prompt("Reset Database, Are you sure? (y/N)", default="N")

    if reset == 'y' or reset == 'Y':
        set_user(superuser=True)
        with settings(warn_only=True):
            execute(Project.reset_env, hosts=env.hosts)


@task
def createsuperuser():
    """
    Create a project superuser in selected server(s).
    """
    set_user(superuser=True)
    with settings(warn_only=True):
        execute(Project.create_superuser, hosts=env.hosts)


@task
def profile():
    local("echo \"export LANG=C.UTF-8\" >> ~/.bash_profile")
    local("echo \"export LC_CTYPE=C.UTF-8\" >> ~/.bash_profile")
    local("echo \"export LC_ALL=C.UTF-8\" >> ~/.bash_profile")


@task
def help():
    print("")
    print("~$ COMMANDS")
    print("-------------------------------------------------------------------------")
    print("")
    print("  - [server] install            Install project into server.")
    print("  - [server] uninstall          Remove project from server.")
    print("  - [server] deploy             Deploy project to server.")
    print("  - [server] restart            Restart project services.")
    print("  - [server] upload_key         Upload SSH key to server.")
    print("  - [server] createsuperuser    Create a superuser for the project in server.")
    print("  - [server] add_remote         Add git remote from server to local git config.")
    print("")
    print("-------------------------------------------------------------------------")


@task
def print_servers():
    print("")
    print("~$ SERVERS")
    print("---------------------------------------------------------------------")
    print("")
    for server in SERVERS.keys():
        print("   -(")+server
    print("")
    print("---------------------------------------------------------------------")
    print("")