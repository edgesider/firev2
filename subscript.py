#! /usr/bin/env python3
from v2ray_config import objects as objs
import sys
import os
import json

import config


# TODO record subscription meta info


def process(type, url, template):
    node_dir = config.node_dir
    template_dir = config.template_dir
    template_path = os.path.join(template_dir, template)

    if type == 'vmess_str':
        pass
    elif type == 'vmess_url':
        os.makedirs(node_dir, exist_ok=True)
        with open(template_path) as f:
            c = json.load(f)
        conf = objs.ConfigObject.from_object(c)
        nodes = objs.outbound.OutboundObject.create(
                'vmess', tag='proxy', url=url,
                gen_list=True)
        for v in nodes:
            conf.outbounds.append(v)
            name = getattr(v.settings.vnext[0], 'ps', None)
            if name is None:
                name = getattr(v.settings.vnext[0], 'address')
            node_path = os.path.join(node_dir, '{}.json'.format(name))
            with open(node_path, 'w') as f:
                json.dump(conf.to_object(ignore_none=True),
                          f, indent=4, ensure_ascii=False)
            conf.outbounds.delete_one(lambda o: o.tag == 'proxy')
    else:
        print("unknown subscription type: {}".format(type))
