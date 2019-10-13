import os
import json


systemd_service = 'firev2.service'
link_target = None
node_dir = None
template_dir = None


def auto_load():
    find_path = [
            'firev2.conf',
            os.path.join(os.environ['HOME'], '.firev2.conf'),
            '/etc/firev2.conf',
            ]
    for f in find_path:
        if os.path.isfile(f):
            load_from_file(f)
            return
    raise Exception('no config file found')


def load_from_file(filename):
    global link_target
    global node_dir
    global template_dir

    with open(filename) as f:
        config = json.load(f)
    node_dir = config['node_dir']
    template_dir = config['template_dir']
    link_target = config['link_target']
