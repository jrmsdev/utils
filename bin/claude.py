#!/usr/bin/env python3
import os
import subprocess
import sys


def ensure_dir(path, mode=0o750):
    os.makedirs(path, mode=mode, exist_ok=True)


def ensure_file(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        open(path, 'w').close()


def container_path(host_path, home, container_home):
    """Map a host path under $HOME to its mirrored container path (lowercased)."""
    rel = os.path.relpath(host_path, home)
    return os.path.join(container_home, rel.lower())


def main():
    user = subprocess.check_output(['id', '-u', '-n']).decode().strip()
    home = os.path.expanduser('~')
    pwd = os.environ.get('PWD', os.getcwd())
    term = os.environ.get('TERM', 'xterm')

    container_home = f'/home/{user}'

    github = os.path.join(home, 'Github')
    temp = os.path.join(home, 'Temp')
    utils = os.path.join(home, 'Utils')
    datadir = os.path.join(home, 'Docker', 'claude')

    for d in [github, temp, utils, os.path.join(home, 'Docker'), datadir,
              os.path.join(datadir, 'config')]:
        ensure_dir(d)

    claude_json = os.path.join(datadir, 'claude.json')
    ensure_file(claude_json)

    # Always-present claude mounts (rw)
    mounts = [
        f'{datadir}/config:{container_home}/.claude',
        f'{claude_json}:{container_home}/.claude.json',
    ]

    entrypoint = '/usr/local/bin/user-login.sh'

    if pwd == home:
        mounts += [
            f'{github}:{container_home}/github:ro',
            f'{temp}:{container_home}/temp',
            f'{utils}:{container_home}/utils',
        ]
        workdir = container_home
    else:
        # Project isolation: mount only current dir + utils + temp
        c_pwd = container_path(pwd, home, container_home)
        mounts += [
            f'{pwd}:{c_pwd}',
            f'{utils}:{container_home}/utils',
            f'{temp}:{container_home}/temp',
        ]
        workdir = c_pwd
        if not (workdir == github or pwd.startswith(github + os.sep)):
            sys.exit(f'error: workdir {pwd!r} must be under $HOME/Github ({github!r})')
        entrypoint = '/usr/local/bin/claude'

    vol_args = []
    for m in mounts:
        vol_args += ['-v', m]

    cmd = [
        'docker', 'run', '-it', '--rm', '-u', user,
        '--hostname', 'claude.debian.local',
        '-e', f'TERM={term}',
        *vol_args,
        '--entrypoint', entrypoint,
        '--workdir', workdir,
        'jrmsdev/claude',
    ]

    os.execvp('docker', cmd)


if __name__ == '__main__':
    main()
