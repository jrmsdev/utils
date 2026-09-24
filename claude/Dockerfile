FROM debian:forky-20260918-slim

LABEL maintainer="Jeremías <jrmsdev@gmail.com>"
LABEL version="260924"

ENV JRMSDEV_UPGRADE=260924

USER root:root
WORKDIR /root

ENV USER=root
ENV HOME=/root

ENV DEBIAN_FRONTEND=noninteractive

COPY apt.install /tmp/apt.install

RUN apt-get clean \
	&& apt-get update -yy \
	&& apt-get dist-upgrade -yy --purge \
	&& cat /tmp/apt.install | xargs apt-get install -yy --no-install-recommends \
	&& apt-get clean \
	&& apt-get autoremove -yy --purge \
	&& rm -rf /var/lib/apt/lists/* \
		/var/cache/apt/archives/*.deb \
		/var/cache/apt/*cache.bin

ARG USER_NAME=jrms
ARG USER_UID=501
ARG USER_GID=20

ENV USER_NAME=${USER_NAME}
ENV USER_UID=${USER_UID}
ENV USER_GID=${USER_GID}

RUN groupadd -o -g "${USER_GID}" "${USER_NAME}" \
	&& useradd -o -d "/home/${USER_NAME}" -m -c "${USER_NAME}" \
		-g "${USER_GID}" -u "${USER_UID}" "${USER_NAME}" \
	&& chmod -v 0750 "/home/${USER_NAME}"

RUN printf 'umask %s\n' '0027' >>"/home/${USER_NAME}/.profile"

RUN echo "${USER_NAME} ALL=(ALL:ALL) NOPASSWD: ALL" >>"/etc/sudoers.d/${USER_NAME}"
RUN chmod -v 0440 "/etc/sudoers.d/${USER_NAME}"

COPY user-login.sh /usr/local/bin/user-login.sh
RUN chmod -v 0755 /usr/local/bin/user-login.sh

RUN ln -vsf /home/${USER_NAME}/.local/bin/claude /usr/local/bin/claude

USER ${USER_NAME}:${USER_NAME}
WORKDIR /home/${USER_NAME}

ENV USER=${USER_NAME}
ENV HOME=/home/${USER_NAME}

RUN bash --version

RUN git config --global alias.st status

ENV JRMSDEV_CLAUDE_UPGRADE=2.1.281

RUN curl -fsSL https://claude.ai/install.sh | bash

RUN /usr/local/bin/claude --version

ENTRYPOINT ["/usr/local/bin/user-login.sh"]
