#! /usr/bin/env python3
from v2ray_config import objects as objs
import sys
import os
import json
from getopt import gnu_getopt as getopt
from getopt import GetoptError

base_dir = os.path.join(os.environ['HOME'], '.config', 'firev2')
node_dir = os.path.join(base_dir, 'nodes')
template_dir = os.path.join(base_dir, 'templates')

usage_str = f"""{sys.argv[0]} TYPE INPUT [OUTPUT]

    supported types | input meaning
    -------------------------------
    vmess_str       | vmess://...
    vmess_url       | http(s) subscription url
"""

def usage():
    print(usage_str, file=sys.stderr)
    exit(-1)

def parse():
    argv = sys.argv[1:]
    if '--help' in sys.argv:
        usage()
    if len(argv) == 3:
        return argv
    if len(argv) == 2:
        argv.append(node_dir)
        return argv
    usage()


if __name__ == '__main__':
    intype, instr, outdir = parse()

    if intype == 'vmess_str':
        pass
    elif intype == 'vmess_url':
        os.makedirs(node_dir, exist_ok=True)
        with open(os.path.join(template_dir, 'proxy_multi.json')) as f:
            c = json.load(f)
        conf = objs.ConfigObject.from_object(c)
        nodes = objs.outbound.OutboundObject.create(
                'vmess', tag='proxy', url=instr,
                gen_list=True)
        for v in nodes:
            conf.outbounds.append(v)
            name = getattr(v.settings.vnext[0], 'ps', None)
            if name is None:
                name = getattr(v.settings.vnext[0], 'address')
            with open(os.path.join(outdir, f'{name}.json'), 'w') as f:
                json.dump(conf.to_object(ignore_none=True),
                        f, indent=4, ensure_ascii=False)
            conf.outbounds.delete_one(lambda o: o.tag == 'proxy')
    else:
        usage()
