from __future__ import unicode_literals
from fabric.api import *

from tasks.config import *


class SuperUser(object):

    @staticmethod
    def username():
        """
        Get superuser from config/credentials.yml.
        """
        return CREDENTIALS[env.stage]["superuser"]

    @staticmethod
    def password():
        """
        Get superuser password from config/credentials.yml.
        """
        return CREDENTIALS[env.stage]["password"]


class Utils(object):
    @staticmethod
    def upload_key():
        """
        Upload  id_rsa.pub file to server.
        This file is obtained from ssh-keygen command.
        """
        try:
            local("ssh-copy-id %s@%s" % (env.user, env.hosts[0]))
        except Exception:
            raise Exception('Unfulfilled local requirements')


def set_stage(stage='develop'):
    if stage in SERVERS.keys():
        env.stage = stage
        env.project = SERVERS[env.stage]["project"]
        env.domain = SERVERS[env.stage]["domain"]
        env.urls = SERVERS[env.stage]["urls"]
        env.docs = SERVERS[env.stage]["docs"]
        env.enginedb = SERVERS[env.stage]["enginedb"]
        env.hosts = [SERVERS[env.stage]["ip_address"], ]
        env.branch = SERVERS[env.stage]["branch"]
        env.team = SERVERS[env.stage]["team"]
        env.home_path = SERVERS[env.stage]["home_path"]
    else:
        pass
        # print_servers()


def set_user(superuser=False):
    if superuser:
        env.user = SuperUser.username()
        env.password = SuperUser.password()
    else:
        env.user = SERVERS[env.stage]["user"]
        env.password = SERVERS[env.stage]["password"]


def isolate_stage(stage):
    if not env.stage == stage:
        raise ValueError('This implementation is only for %s STAGE' % stage.upper())

