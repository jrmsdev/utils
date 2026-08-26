#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys


CONFIG_PATH = os.path.expanduser('~/.config/jrmsdev/claude.json')


def ensure_dir(path, mode=0o750):
    os.makedirs(path, mode=mode, exist_ok=True)


def ensure_file(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        open(path, 'w').close()


def container_path(host_path, home, container_home):
    """Map a host path under $HOME to its mirrored container path (lowercased)."""
    rel = os.path.relpath(host_path, home)
    return os.path.join(container_home, rel.lower())


def load_config(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        sys.exit(f'error: configuration file not found: {path!r}')
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f'error: cannot read configuration {path!r}: {exc}')

    if not isinstance(config, dict):
        sys.exit(f'error: configuration root must be a JSON object: {path!r}')

    paths = config.get('allowed_mount_paths', [])
    if not isinstance(paths, list):
        sys.exit('error: "allowed_mount_paths" must be a JSON array')

    return paths


def parse_mount_spec(spec):
    """Parse PATH[:ro|rw], with rw as the default."""
    if not isinstance(spec, str) or not spec:
        raise ValueError('mount path must be a non-empty string')

    path, sep, mode = spec.rpartition(':')
    if not sep:
        path, mode = spec, 'rw'
    elif mode not in ('ro', 'rw') or not path:
        raise ValueError(
            f'invalid mount specification {spec!r}; '
            f'expected PATH, PATH:ro, or PATH:rw'
        )

    path = os.path.abspath(os.path.expanduser(path))
    return path, mode


def validate_mount_path(path, home, uid):
    """
    Return the canonical path after validating that it exists and is owned
    by the invoking user.

    Canonicalization is intentional: Docker receives the resolved path,
    rather than a path containing a symlink that could escape the path
    we validated.
    """
    try:
        real = os.path.realpath(path)
        st = os.stat(real)
    except OSError as exc:
        raise ValueError(
            f'cannot access allowed mount path {path!r}: {exc}'
        ) from exc

    if st.st_uid != uid:
        raise ValueError(
            f'allowed mount path {path!r} is not owned by the current user'
        )

    # Do not allow an allowed path to escape the user's home through symlinks.
    try:
        common = os.path.commonpath((real, home))
    except ValueError:
        common = None
    if common != home:
        raise ValueError(
            f'allowed mount path {path!r} resolves outside $HOME: {real!r}'
        )

    return real


def path_is_under(path, parent):
    try:
        return os.path.commonpath((path, parent)) == parent
    except ValueError:
        return False


def load_allowed_mounts(config_path, home, uid):
    specs = load_config(config_path)
    mounts = []

    for spec in specs:
        try:
            path, mode = parse_mount_spec(spec)
            real = validate_mount_path(path, home, uid)
        except ValueError as exc:
            sys.exit(f'error: {exc}')

        mounts.append((real, mode))

    # Reject nested entries. They create overlapping Docker mounts and make
    # the resulting container view unnecessarily difficult to reason about.
    for i, (path, _) in enumerate(mounts):
        for j, (other, _) in enumerate(mounts):
            if i != j and path_is_under(path, other):
                sys.exit(
                    f'error: overlapping allowed mount paths: '
                    f'{path!r} and {other!r}'
                )

    # Also reject duplicate container destinations (e.g. case-only differences).
    destinations = {}
    container_home = f'/home/{os.path.basename(home)}'
    for path, _ in mounts:
        destination = container_path(path, home, container_home)
        if destination in destinations:
            sys.exit(
                f'error: allowed mount paths map to the same container path: '
                f'{path!r} and {destinations[destination]!r}'
            )
        destinations[destination] = path

    return mounts


def main():
    parser = argparse.ArgumentParser(description='Run the claude container.')
    parser.add_argument(
        '--config', action='store_true',
        help='print the docker mounts/volumes needed for claude internal '
             'files, then exit without running the container',
    )
    args = parser.parse_args()

    user = subprocess.check_output(['id', '-u', '-n']).decode().strip()
    uid = os.getuid()
    home = os.path.realpath(os.path.expanduser('~'))

    # Use the actual current working directory, not $PWD, because $PWD is
    # merely an environment variable and can be spoofed.
    pwd = os.path.realpath(os.getcwd())
    term = os.environ.get('TERM', 'xterm')

    container_home = f'/home/{user}'

    # Example configuration:
    #
    # {
    #   "allowed_mount_paths": [
    #     "~/Github:ro",
    #     "~/Projects",
    #     "~/Secrets:ro"
    #   ]
    # }
    #
    # A missing mode means rw.
    allowed_mounts = load_allowed_mounts(CONFIG_PATH, home, uid)

    temp = os.path.join(home, 'Temp')
    utils = os.path.join(home, 'Utils')
    datadir = os.path.join(home, 'Docker', 'claude')

    for d in [
        temp,
        utils,
        os.path.join(home, 'Docker'),
        datadir,
        os.path.join(datadir, 'config'),
    ]:
        ensure_dir(d)

    claude_json = os.path.join(datadir, 'claude.json')
    ensure_file(claude_json)

    # Always-present claude mounts (rw)
    mounts = [
        f'{datadir}/config:{container_home}/.claude',
        f'{claude_json}:{container_home}/.claude.json',
    ]

    if args.config:
        print('claude internal files mounts:')
        for m in mounts:
            print(f'  -v {m}')

        print('configured allowed mounts:')
        for path, mode in allowed_mounts:
            print(
                f'  -v {path}:'
                f'{container_path(path, home, container_home)}:{mode}'
            )
        return

    entrypoint = '/usr/local/bin/user-login.sh'

    if pwd == home:
        mounts += [
            f'{temp}:{container_home}/temp',
            f'{utils}:{container_home}/utils:ro',
        ]
        workdir = container_home
    else:
        # Project isolation: mount only the current directory + utils + temp.
        # The current directory must be contained by a configured path.
        allowed_parent = next(
            (
                (path, mode)
                for path, mode in allowed_mounts
                if path_is_under(pwd, path)
            ),
            None,
        )

        if allowed_parent is None:
            sys.exit(
                f'error: workdir {pwd!r} is not under any configured '
                f'allowed_mount_path'
            )

        _, mode = allowed_parent
        c_pwd = container_path(pwd, home, container_home)

        # Preserve the configured permission. In particular, a :ro parent
        # must not become writable merely because the current directory is
        # mounted separately.
        mounts += [
            f'{pwd}:{c_pwd}:{mode}',
            f'{utils}:{container_home}/utils:ro',
            f'{temp}:{container_home}/temp',
        ]
        workdir = c_pwd
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
