FROM jrmsdev/debian-forky:latest

LABEL maintainer="Jeremías <jrmsdev@gmail.com>"
LABEL version="260422"

ENV JRMSDEV_UPGRADE=260422

USER root:root
WORKDIR /root

ENV USER=root
ENV HOME=/root

ENV DEBIAN_FRONTEND=noninteractive

COPY apt.install /tmp/apt.install

RUN apt-get clean \
	&& apt-get update -yy \
	&& cat /tmp/apt.install | xargs apt-get install -yy --no-install-recommends \
	&& apt-get clean \
	&& apt-get autoremove -yy --purge \
	&& rm -rf /var/lib/apt/lists/* \
		/var/cache/apt/archives/*.deb \
		/var/cache/apt/*cache.bin \
		/tmp/apt.install

USER ${USER_NAME}:${USER_NAME}
WORKDIR /home/${USER_NAME}

ENV USER=${USER_NAME}
ENV HOME=/home/${USER_NAME}

RUN bash --version

ENTRYPOINT ["/usr/local/bin/user-login.sh"]
