import os
import json
import subprocess


systemd_service = 'firev2.service'
link_target = None
node_dir = None
template_dir = None

user = os.environ.get('SUDO_USER')
if user is None:
    home = os.environ['HOME']
else:
    # running as sudo
    home = subprocess.Popen(
            'getent passwd {} | cut -d: -f6'.format(user),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True).communicate()[0].decode('utf8').strip()
find_path = [
        'firev2.conf',
        os.path.join(home, '.config', 'firev2', 'firev2.conf'),
        '/etc/firev2.conf',
        ]

def auto_load():
    for f in find_path:
        if os.path.isfile(f):
            load_from_file(f)
            return
    raise Exception('no config file found')


def load_from_file(filename):
    global link_target
    global node_dir
    global template_dir

    path = os.path.abspath(filename)
    config_dir = os.path.dirname(path)
    config = os.path.basename(path)
    os.chdir(config_dir)
    with open(config) as f:
        config = json.load(f)
    node_dir = os.path.abspath(config['node_dir'])
    template_dir = os.path.abspath(config['template_dir'])
    link_target = os.path.abspath(config['link_target'])
