# Configuration file for Jupyter Hub
c = get_config()

import os
import sys
sys.path.insert(0, '/srv/jupyterhub_config')

# Base configuration
c.JupyterHub.log_level = "INFO"
c.JupyterHub.db_url = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ['JPY_DB_USER'],
    os.environ['JPY_DB_PASSWORD'],
    os.environ['POSTGRES_PORT_5432_TCP_ADDR'],
    os.environ['POSTGRES_PORT_5432_TCP_PORT'],
    os.environ['JPY_DB_NAME']
)
c.JupyterHub.admin_access = True
c.JupyterHub.confirm_no_ssl = True

# Configure the authenticator (Github)
c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
c.GitHubOAuthenticator.oauth_callback_url = os.environ['JUPYTERHUB_OAUTH_CALLBACK_URL']
c.GitHubOAuthenticator.client_id = os.environ['JUPYTERHUB_OAUTH_CLIENT_ID']
c.GitHubOAuthenticator.client_secret = os.environ['JUPYTERHUB_OAUTH_CLIENT_SECRET']
c.LocalAuthenticator.create_system_users = True
c.Authenticator.admin_users = admin = set()
c.Authenticator.whitelist = whitelist = set()

# Configure the spawner
c.JupyterHub.spawner_class = 'systemuserspawner.SystemUserSpawner'
c.DockerSpawner.container_image = 'compmodels/systemuser'
c.DockerSpawner.tls_cert = os.environ['DOCKER_TLS_CERT']
c.DockerSpawner.tls_key = os.environ['DOCKER_TLS_KEY']
c.DockerSpawner.remove_containers = True
c.DockerSpawner.volumes = {os.environ['NBGRADER_EXCHANGE']: os.environ['NBGRADER_EXCHANGE']}
c.DockerSpawner.extra_host_config = {'mem_limit': '1g'}
c.DockerSpawner.container_ip = "0.0.0.0"

# The docker instances need access to the Hub, so the default loopback port
# doesn't work. We need to tell the hub to listen on 0.0.0.0 because it's in a
# container, and we'll expose the port properly when the container is run. Then,
# we explicitly tell the spawned containers to connect to the proper IP address.
c.JupyterHub.proxy_api_ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'
c.DockerSpawner.hub_ip_connect = '0.0.0.0'

# Add users to the admin list, the whitelist, and also record their user ids
with open('/srv/jupyterhub_users/userlist') as f:
    for line in f:
        if line.isspace():
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)
