#! /usr/bin/env python3

import os
import sys
import subprocess

import config


service_path = '/lib/systemd/system/firev2.service'
template = """[Unit]
Description=FireV2 Service
After=network.target
Wants=network.target

[Service]
Type=simple
Environment=V2RAY_LOCATION_ASSET=/etc/v2ray
ExecStart={} -config {}
Restart=on-failure
RestartPreventExitStatus=23

[Install]
WantedBy=multi-user.target
"""

def get_v2ray_path():
    p = subprocess.Popen(
            ['which', 'v2ray'],
            stdout=subprocess.PIPE)
    output = p.communicate()[0]
    if p.returncode != 0:
        raise Exception('v2ray not found')
    return output.decode('utf8').strip()

def get_using_node():
    config.auto_load()
    return config.link_target

def get_service_content():
    return template.format(get_v2ray_path(), get_using_node())

def daemon_reload():
    subprocess.Popen(['systemctl', 'daemon-reload']).communicate()


if __name__ == '__main__':
    content = get_service_content()
    if os.path.exists(service_path):
        if input('{} existed. Continue? [y/N]: ' \
                .format(service_path)).strip().lower() != 'y':
            sys.exit(-1)
    with open(service_path, 'w') as f:
        f.write(content)
    daemon_reload()
