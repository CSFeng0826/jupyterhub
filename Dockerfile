FROM jupyterhub/jupyterhub

MAINTAINER Jessica Hamrick <jhamrick@berkeley.edu>

# We need to update pip, otherwise the version of requests that
# is installed by dockerspawner breaks things.
RUN pip install --upgrade pip

# Install dockerspawner, oauthenticator and psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev \
    build-essential \
    python-dev \
    python3-dev \
    && pip install docker-py==1.9.0 \
    dockerspawner \
    oauthenticator \
    psycopg2

# add the userlist, spawner, and authenticator
RUN mkdir /srv/jupyterhub_config
WORKDIR /srv/jupyterhub_config
ADD systemuserspawner.py /srv/jupyterhub_config/systemuserspawner.py
ADD docker_oauth.py /srv/jupyterhub_config/docker_oauth.py
ADD jupyterhub_config.py /srv/jupyterhub_config/jupyterhub_config.py

# create /srv/jupyterhub_users directory (which is where we'll mount the userlist)
RUN mkdir /srv/jupyterhub_users
ADD userlist /srv/jupyterhub_users/userlist

# we need to expose ports for the hub api and for the proxy api
EXPOSE 8080
EXPOSE 8001

# environment variable for swarm
ENV DOCKER_HOST https://swarm:2375

# run jupyterhub
ENTRYPOINT ["jupyterhub", "-f", "/srv/jupyterhub_config/jupyterhub_config.py"]