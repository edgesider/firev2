import os
import subprocess

import config


def get_nodes():
    files = os.listdir(config.node_dir)
    return [f.replace('.json', '') for f in files if f.endswith('.json')]


def get_node_path(node_name):
    return os.path.join(
            config.node_dir, '{}.json'.format(node_name))


def check_node(node):
    nodepath = get_node_path(node)
    if not os.path.isfile(nodepath):
        raise FileNotFoundError(
                'node file "{}" not found'.format(nodepath))


def create_link(node):
    nodepath = get_node_path(node)
    target = config.link_target
    if os.path.islink(target):
        os.remove(target)
    os.symlink(nodepath, target)


def systemd_restart():
    p = subprocess.Popen(
            ['systemctl', 'restart',
                config.systemd_service])
    p.communicate()
    if p.returncode != 0:
        raise Exception('restart failed')


def systemd_stop():
    p = subprocess.Popen(
            ['systemctl', 'stop',
                config.systemd_service])
    p.communicate()
    if p.returncode != 0:
        raise Exception('stop failed')


def systemd_status():
    p = subprocess.Popen(
            ['systemctl', 'status',
                config.systemd_service, '--no-pager'])
    p.communicate()


def process_start(node):
    check_node(node)
    create_link(node)
    systemd_restart()


def process_restart():
    systemd_restart()


def process_stop():
    systemd_stop()


def process_status():
    print('current use: {}'.format(
        os.readlink(config.link_target)))
    systemd_status()


def process_list():
    for n in get_nodes():
        print(n)
