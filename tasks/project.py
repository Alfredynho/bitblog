from __future__ import unicode_literals
from fabric.api import *
from fabric.contrib.files import upload_template

from tasks.config import *


class Project(object):

    @staticmethod
    def push():
        """ Push changes to selected server"""
        local("git push %s %s" % (env.stage, env.branch))

    @staticmethod
    def environment():
        """ Push the environment configuration """
        with lcd("./config"):
            with cd("%s/config" % get_project_path(env.stage)):
                upload_template(
                    filename="./.environment",
                    destination='./.environment',
                    template_dir="./",
                    use_sudo=False,
                )

    @staticmethod
    def reload():
        """
        Run intall command.
        """
        with cd(get_project_path(env.stage)):
            run("make reload SETTINGS=settings.production")


    @staticmethod
    def start():
        """
        Start supervisor service.
        """
        sudo("supervisorctl start %s" % env.project)

    @staticmethod
    def create_superuser():
        """
        Create a superuser to production at selected server.
        """
        with settings(user=SERVERS[env.stage]["user"], password=SERVERS[env.stage]["password"]):
            with cd(get_project_path(env.stage)):
                run("make superuser SETTINGS=settings.production")

    @staticmethod
    def reset_env():
        """
        Create a superuser to production at selected server.
        """
        with settings(user=SERVERS[env.stage]["user"], password=SERVERS[env.stage]["password"]):
            with cd(get_project_path(env.stage)):
                run("rm -rf env/")

    @staticmethod
    def restart():
        """
        Restart supervisor service.
        """
        sudo("supervisorctl restart %s" % env.project)

    @staticmethod
    def stop():
        """
        Stop supervisor service.
        """
        sudo("supervisorctl stop %s" % env.project)

    @staticmethod
    def clean_cache():
        """
        Clean project cache.
        """
        with cd("%s/var/cache" % get_project_path(env.stage)):
            run("rm -rf *")

    @staticmethod
    def clean_logs():
        """
        Clean project logs.
        """
        with cd("%s/var/log" % get_project_path(env.stage)):
            run("rm -rf *")