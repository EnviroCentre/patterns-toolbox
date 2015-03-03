# -*- coding: utf-8 -*-

from subprocess import check_output, CalledProcessError
from codecs import open
from os import path

TAG_PREFIX = 'v'


def update():
    here = path.abspath(path.dirname(__file__))

    try:
        git_args = ['git',
                    'describe',
                    '--tags',
                    '--always']
        v_elements = check_output(git_args, universal_newlines=True).split('-')

        tag = v_elements[0]
        if not tag.startswith(TAG_PREFIX):
            raise ValueError("Tag `{}` must start with `{}`.".format(tag, TAG_PREFIX))
        version = tag[len(TAG_PREFIX):].strip()

        if len(v_elements) == 1:
            v_str = version
            dist = 0
        else:
            dist = v_elements[1].strip()
            v_str = '+'.join([version, dist])

        with open(path.join(here, 'VERSION'), mode='w', encoding='utf-8') as v_file:
            v_file.write(v_str)

        return {'tag': version,
                'dist': dist,
                'str': v_str}

    except CalledProcessError:
        # If we're not in a git repo, get the version from the VERSION file

        v_str = open(path.join(here, 'VERSION'), encoding='utf-8').read().strip()
        v_elements = v_str.split('-')
        tag = v_elements[0]
        if len(v_elements) == 1:
            dist = 0
        else:
            dist = v_elements[1]
        return {'tag': tag,
                'dist': dist,
                'str': v_str}
