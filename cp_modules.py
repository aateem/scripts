from configparser import ConfigParser
import subprocess
import sys
import base64

import requests


BASE_GH_URL = 'https://api.github.com'
PACK_PATH = 'pack/aateem/opt'


def _run_git_cmd(name: str, url: str, path: str):
    command = [
            'git', 'submodule', 'add',
            '--name', name,
            url,
            path,
            ]
    run_cmd = subprocess.run(command)


def _get_submodule_config():
    user, repo = sys.argv[1:3]
    headers = {'accept': 'application/vnd.github.v3+json'}
    path = '.gitmodules'
    url = '/'.join([BASE_GH_URL, 'repos', user, repo, 'contents', path])
    content = requests.get(url, headers=headers).json()['content']
    config = ConfigParser()
    config.read_string(base64.b64decode(content).decode(encoding='utf-8'))
    return config


def add_submodules(config: ConfigParser, root_path: str):
    for section in config.sections():
        name = section.split(' ')[1].strip("\"")
        url = config[section]['url']
        import pathlib
        path = pathlib.PurePath(root_path, PACK_PATH, name).as_posix()
        _run_git_cmd(name, url, path)


if __name__ == "__main__":
   config = _get_submodule_config()
   add_submodules(config, './')
   