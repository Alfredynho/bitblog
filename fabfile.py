from __future__ import unicode_literals

from tools.tasks.config import _upload_key
from tools.tasks.server import *
from tools.tasks.project import *


# ~$ ENVIRONMENTS
# ---------------------------------------------------------------------

@task
def read():
    get_config()


@task
def production():
    set_stage('production')


@task
def develop():
    set_stage('develop')


@task
def test():
    set_stage('test')


# ~$ COMMANDS
# ---------------------------------------------------------------------

@task
def upgrade():
    set_user(superuser=True)
    with settings(hide('warnings'), warn_only=True, ):
        execute(Server.upgrade, hosts=env.hosts)


@task
def install():
    """
    Install app in selected server(s).
    """

    set_user(superuser=True)
    with settings(hide('warnings'), warn_only=True, ):
        execute(Server.deps, hosts=env.hosts)
        execute(Server.user, hosts=env.hosts)
        execute(Server.group, hosts=env.hosts)
        execute(Server.create_db, hosts=env.hosts)
        execute(Server.git, hosts=env.hosts)
        execute(Server.add_remote, hosts=env.hosts)
        execute(Server.nginx, hosts=env.hosts)
        execute(Server.gunicorn, hosts=env.hosts)
        execute(Server.supervisor, hosts=env.hosts)
        execute(Server.letsencrypt, hosts=env.hosts)
        execute(Server.var, hosts=env.hosts)
        execute(Server.pip_cache, hosts=env.hosts)
        execute(Server.fix_permissions, hosts=env.hosts)


@task
def uninstall():
    """
    Uninstall app in selected server(s)
    """
    set_user(superuser=True)
    with settings(hide('warnings'), warn_only=True, ):
        execute(Server.clean, hosts=env.hosts)

@task
def restart():
    """
    Restart all app services.
    """
    set_user(superuser=True)
    with settings(hide('warnings'), warn_only=True, ):
        execute(Server.restart_services, hosts=env.hosts)


@task()
def deploy():
    """
    Deploy application in selected server(s)
    """
    set_user()
    with settings(hide('warnings'), warn_only=True, ):
        execute(Project.push, hosts=env.hosts)
        execute(Project.environment, hosts=env.hosts)
        execute(Project.install, hosts=env.hosts)
        execute(Project.clean, hosts=env.hosts)


@task()
def load_corpus():
    """
    Load nltk corpus
    """
    set_user()
    with settings(hide('warnings'), warn_only=True, ):
        execute(Project.load_corpus, hosts=env.hosts)


@task
def fix_permissions():
    """
    Add project repo url to local git configuration.
    """
    set_user(superuser=True)
    with settings(hide('warnings'), warn_only=True, ):
        execute(Server.fix_permissions, hosts=env.hosts)


@task
def add_remote():
    """
    Add project repo url to local git configuration.
    """
    with settings(hide('warnings'), warn_only=True, ):
        execute(Server.add_remote, hosts=env.hosts)


@task
def upload_key():
    """
    Upload SSH key to server.
    """
    set_user()
    with settings(hide('warnings'), warn_only=True, ):
        execute(_upload_key, hosts=env.hosts)


@task
def reset_db():
    """
    Reset the env Database
    """
    reset = prompt("Reset Database, Are you sure? (y/N)", default="N")

    if reset == 'y' or reset == 'Y':
        set_user(superuser=True)
        with settings(hide('warnings'), warn_only=True, ):
            execute(Server.reset_db, hosts=env.hosts)


@task
def reset_env():
    """
    Reset the python env
    """
    reset = prompt("Reset Database, Are you sure? (y/N)", default="N")

    if reset == 'y' or reset == 'Y':
        set_user(superuser=True)
        with settings(hide('warnings'), warn_only=True, ):
            execute(Project.reset_env, hosts=env.hosts)


@task
def list_droplets():
    config, manager = get_digitalocean_config()
    for droplet in manager.get_all_droplets():
        print(droplet.name + ' ---> ' + droplet.ip_address)


@task
def new_droplet():
    try:
        import digitalocean
        config, manager = get_digitalocean_config()
        keys = manager.get_all_sshkeys()
        droplet = digitalocean.Droplet(
            token=config["token"],
            name=config["name"],
            region=config["region"],
            image=config["image"],
            size_slug=config["ram"],
            ssh_keys=keys,
            backups=False,
        )
        droplet.create()
    except Exception:
        pass


@task
def drop_droplet():
    try:
        import digitalocean
        config, manager = get_digitalocean_config()
        for droplet in manager.get_all_droplets():
            if droplet.name == config["name"]:
                droplet.destroy()
                print("[%s] is destroyed!" % config["name"])
    except Exception:
        pass


@task
def createsuperuser():
    """
    Create a project superuser in selected server(s).
    """
    set_user(superuser=True)
    with settings(hide('warnings'), warn_only=True, ):
        execute(Project.create_superuser, hosts=env.hosts)


@task
def createcorpora():
    """
    Install NLTK Copora
    """
    set_user(superuser=True)
    with settings(hide('warnings'), warn_only=True, ):
        execute(Project.corpora, hosts=env.hosts)


@task
def profile():
    local("echo \"export LANG=C.UTF-8\" >> ~/.bash_profile")
    local("echo \"export LC_CTYPE=C.UTF-8\" >> ~/.bash_profile")
    local("echo \"export LC_ALL=C.UTF-8\" >> ~/.bash_profile")


@task
def add_certificate(domain=None):
    set_user(superuser=True)
    with settings(hide('warnings'), warn_only=True, ):
        if domain:
            execute(Server.letsencrypt, domain, hosts=env.hosts)
        else:
            raise Exception("The domain param is required!")


@task
def help():
    print("")
    print("~$ COMMANDS")
    print("-------------------------------------------------------------------------")
    print("")
    print("  - [server] install                 Install project into server.")
    print("  - [server] uninstall               Remove project from server.")
    print("  - [server] deploy                  Deploy project to server.")
    print("  - [server] restart                 Restart project services.")
    print("  - [server] upload_key              Upload SSH key to server.")
    print("  - [server] createsuperuser         Create a superuser for the project in server.")
    print("  - [server] add_remote              Add git remote from server to local git config.")
    print("  - [server] profile                 Set language ENV Variables")
    print("  - [server] add_certificate:DOMAIN  add SSL Certificates via letsencrypt")
    print("")
    print("-------------------------------------------------------------------------")
