from objects import (inbound, outbound, routing,
                     config)
from objects.protocol import (blackhole, freedom, vmess,
                              shadowsocks, socks)


def pprint(d):
    import pprint
    pprint.pprint(d)
    # print(json.dumps(d, ensure_ascii=False, indent=4))


def test_outbound_freedom():
    f = freedom.FreedomOutboundSettingObject.from_object({})
    assert f.to_object() == {
        "domainStrategy": None,
        "redirect": None,
        "user_level": None
    }


def test_outbound_blackhole():
    b = blackhole.BlackholeOutboundSettingObject.from_object({})
    assert b.to_object() == {}


def test_outbound_vmess():
    v = vmess.VmessOutboundSettingObject.from_object(
        {
            "vnext": [
                {
                    "address": "127.0.0.1",
                    "port": 37192,
                    "users": [
                        {
                            "id": "27848739-7e62-4138-9fd3-098a63964b6b",
                            "alterId": 4,
                            "security": "auto",
                            "level": 0
                        }
                    ],
                    "ps": "ps"
                }
            ]
        }
    )
    assert v.to_object() == {'vnext': [{'address': '127.0.0.1',
                                        'port': 37192,
                                        'ps': 'ps',
                                        'users': [{'alterId': 4,
                                                   'id': '27848739-7e62-4138-9fd3-098a63964b6b',
                                                   'level': 0,
                                                   'security': 'auto'}]}]}


def test_outbound_socks():
    pass


def test_outbound_shadowsocks():
    s = shadowsocks.ShadowsocksOutboundSettingObject.from_object({
        'servers': [{
            "email": "love@v2ray.com",
            "address": "127.0.0.1",
            "port": 1234,
            "method": "加密方式",
            "password": "密码",
            "ota": False,
            "level": 0
        }]})
    assert s.to_object() == {'servers': [{'address': '127.0.0.1',
                                          'email': 'love@v2ray.com',
                                          'level': 0,
                                          'method': '加密方式',
                                          'ota': False,
                                          'password': '密码',
                                          'port': 1234}]}


def test_inbound_vmess():
    v = vmess.VmessInboundSettingObject.from_object({
        "clients": [
            {
                "id": "27848739-7e62-4138-9fd3-098a63964b6b",
                "level": 0,
                "alterId": 4,
                "email": "love@v2ray.com"
            }
        ],
        "default": {
            "level": 0,
            "alterId": 4
        },
        "detour": {
            "to": "tag_to_detour"
        },
        "disableInsecureEncryption": False
    })
    assert v.to_object() == {
        "clients": [
            {
                "id": "27848739-7e62-4138-9fd3-098a63964b6b",
                "level": 0,
                "alterId": 4,
                "email": "love@v2ray.com"
            }
        ],
        "disableInsecureEncryption": False,
        "default": {
            "level": 0,
            "alterId": 4
        },
        "detour": {
            "to": "tag_to_detour"
        }
    }


def test_inbound_socks():
    s = socks.SocksInboundSettingObject.from_object({
        "auth": "noauth",
        "accounts": [
            {
                "user": "my-username",
                "pass": "my-password"
            }
        ],
        "udp": False,
        "ip": "127.0.0.1",
        "userLevel": 0
    })
    assert s.to_object() == {'accounts': [{'pass': 'my-password', 'user': 'my-username'}],
                             'auth': 'noauth',
                             'ip': '127.0.0.1',
                             'udp': False,
                             'userLevel': 0}


def test_inbound_shadowsocks():
    s = shadowsocks.ShadowsocksInboundSettingObject.from_object({
        "email": "love@v2ray.com",
        "method": "aes-128-cfb",
        "password": "密码",
        "level": 0,
        "ota": True,
        "network": "tcp"
    })
    assert s.to_object() == {'email': 'love@v2ray.com',
                             'level': 0,
                             'method': 'aes-128-cfb',
                             'network': 'tcp',
                             'ota': True,
                             'password': '密码'}


def test_inbound():
    i = inbound.InboundObject.from_object({
        "port": 1080,
        "listen": "127.0.0.1",
        "protocol": "socks",
        "settings": {
            "auth": "noauth",
            "accounts": [
                {
                    "user": "my-username",
                    "pass": "my-password"
                }
            ],
            "udp": False,
            "ip": "127.0.0.1",
            "userLevel": 0
        },
        "streamSettings": {},
        "tag": "fq",
        "sniffing": {
            "enabled": False,
            "destOverride": None
        },
        "allocate": {
            "strategy": "always",
            "refresh": 5,
            "concurrency": 3
        }
    })
    assert i.to_object() == {'allocate': "{'strategy': 'always', 'refresh': 5, 'concurrency': 3}",
                             'listen': '127.0.0.1',
                             'port': 1080,
                             'protocol': 'socks',
                             'settings': {'accounts': [{'pass': 'my-password', 'user': 'my-username'}],
                                          'auth': 'noauth',
                                          'ip': '127.0.0.1',
                                          'udp': False,
                                          'userLevel': 0},
                             'sniffing': {'destOverride': None, 'enabled': False},
                             'streamSettings': {'network': None, 'security': None, 'sockopt': None},
                             'tag': 'fq'}


def test_outbound():
    o = outbound.OutboundObject.from_object({
        "tag": "fq",
        "protocol": "vmess",
        "streamSettings": {
            "network": "ws",
            "security": "none",
            "tls": {}
        },
        "settings": {
            "vnext": [
                {
                    "address": "us1.top",
                    "port": 80,
                    "ps": "ps",
                    "users": [
                        {
                            "id": "Token",
                            "alterId": 64,
                            "security": "auto",
                            "level": 0
                        }
                    ]
                },
                {
                    "address": "hk4.top",
                    "port": 888,
                    "ps": "ps",
                    "users": [
                        {
                            "id": "Token",
                            "alterId": 64,
                            "security": "auto",
                            "level": 0
                        }
                    ]
                },
            ]
        }
    })
    assert o.to_object() == {'protocol': 'vmess',
                             'proxySettings': None,
                             'sendThrough': None,
                             'settings': {'vnext': [{'address': 'us1.top',
                                                     'port': 80,
                                                     "ps": "ps",
                                                     'users': [{'alterId': 64,
                                                                'id': 'Token',
                                                                'level': 0,
                                                                'security': 'auto'}]},
                                                    {'address': 'hk4.top',
                                                     'port': 888,
                                                     "ps": "ps",
                                                     'users': [{'alterId': 64,
                                                                'id': 'Token',
                                                                'level': 0,
                                                                'security': 'auto'}]}]},
                             'streamSettings': {'network': 'ws', 'security': 'none', 'sockopt': None},
                             'tag': 'fq'}


def test_routing_rule():
    r = routing.RuleObject.from_object({
        "type": "field",
        "domain": [
            "baidu.com",
            "qq.com",
            "geosite:cn"
        ],
        "ip": [
            "0.0.0.0/8",
            "10.0.0.0/8",
            "fc00::/7",
            "fe80::/10",
            "geoip:cn"
        ],
        "port": "53,443,1000-2000",
        "network": "tcp",
        "source": [
            "10.0.0.1"
        ],
        "user": [
            "love@v2ray.com"
        ],
        "inboundTag": [
            "tag-vmess"
        ],
        "protocol": ["http", "tls", "bittorrent"],
        "attrs": "attrs[':method'] == 'GET'",
        "outboundTag": "direct",
        "balancerTag": "balancer"
    })
    assert r.to_object() == {'attrs': "attrs[':method'] == 'GET'",
                             'balancerTag': 'balancer',
                             'domain': ['baidu.com', 'qq.com', 'geosite:cn'],
                             'inboundTag': ['tag-vmess'],
                             'ip': ['0.0.0.0/8', '10.0.0.0/8', 'fc00::/7', 'fe80::/10', 'geoip:cn'],
                             'network': 'tcp',
                             'outboundTag': 'direct',
                             'port': '53,443,1000-2000',
                             'protocol': ['http', 'tls', 'bittorrent'],
                             'source': ['10.0.0.1'],
                             'type': 'field',
                             'user': ['love@v2ray.com']}


def test_routing_balancer():
    b = routing.BalancerObject.from_object({
        "tag": "balancer",
        "selector": ["a", "b"]
    })
    assert b.to_object() == {'selector': ['a', 'b'], 'tag': 'balancer'}


def test_routing():
    r = routing.RoutingObject.from_object({
        'domainStrategy': 'AsIs',
        'rules': [{
            "type": "field",
            "domain": [
                "baidu.com",
                "qq.com",
                "geosite:cn"
            ],
            "ip": [
                "0.0.0.0/8",
                "10.0.0.0/8",
                "fc00::/7",
                "fe80::/10",
                "geoip:cn"
            ],
            "port": "53,443,1000-2000",
            "network": "tcp",
            "source": [
                "10.0.0.1"
            ],
            "user": [
                "love@v2ray.com"
            ],
            "inboundTag": [
                "tag-vmess"
            ],
            "protocol": ["http", "tls", "bittorrent"],
            "attrs": "attrs[':method'] == 'GET'",
            "outboundTag": "direct",
            "balancerTag": "balancer"
        }],
        'balancers': [
            {
                "tag": "balancer1",
                "selector": ["a", "b", "c"]
            }
        ]
    })
    assert r.to_object() == {'balancers': [{'selector': ['a', 'b', 'c'], 'tag': 'balancer1'}],
                             'domainStrategy': 'AsIs',
                             'rules': [{'attrs': "attrs[':method'] == 'GET'",
                                        'balancerTag': 'balancer',
                                        'domain': ['baidu.com', 'qq.com', 'geosite:cn'],
                                        'inboundTag': ['tag-vmess'],
                                        'ip': ['0.0.0.0/8',
                                               '10.0.0.0/8',
                                               'fc00::/7',
                                               'fe80::/10',
                                               'geoip:cn'],
                                        'network': 'tcp',
                                        'outboundTag': 'direct',
                                        'port': '53,443,1000-2000',
                                        'protocol': ['http', 'tls', 'bittorrent'],
                                        'source': ['10.0.0.1'],
                                        'type': 'field',
                                        'user': ['love@v2ray.com']}]}


def test_config():
    obj = {
        "log": {
            "access": "/var/log/v2ray/access.log",
            "error": "/var/log/v2ray/error.log",
            "loglevel": "warn"
        },
        "inbounds": [
            {
                "tag": "auto",
                "port": 1079,
                "listen": "127.0.0.1",
                "protocol": "socks",
                "settings": {
                    "auth": "noauth",
                    "udp": False,
                    "ip": "127.0.0.1",
                    "userLevel": 0
                }
            },
            {
                "tag": "fq",
                "port": 1080,
                "listen": "127.0.0.1",
                "protocol": "socks",
                "settings": {
                    "auth": "noauth",
                    "udp": False,
                    "ip": "127.0.0.1",
                    "userLevel": 0
                }
            }
        ],
        "outbounds": [
            {
                "tag": "direct",
                "protocol": "freedom",
                "settings": {}
            },
            {
                "tag": "blocked",
                "protocol": "blackhole",
                "settings": {}
            },
            {
                "tag": "fq",
                "protocol": "vmess",
                "streamSettings": {
                    "network": "ws",
                    "security": "none",
                    "tls": {}
                },
                "settings": {
                    "vnext": [
                        {
                            "address": "us1.top",
                            "port": 80,
                            "users": [
                                {
                                    "id": "token",
                                    "alterId": 64,
                                    "security": "auto",
                                    "level": 0
                                }
                            ]
                        },
                        {
                            "address": "us2.top",
                            "port": 80,
                            "users": [
                                {
                                    "id": "token",
                                    "alterId": 64,
                                    "security": "auto",
                                    "level": 0
                                }
                            ]
                        }
                    ]
                }
            }
        ],
        "routing": {
            "domainStrategy": "AsIs",
            "rules": [
                {
                    "type": "field",
                    "inboundTag": "fq",
                    "outboundTag": "fq"
                },
                {
                    "type": "field",
                    "domain": [
                        "geosite:geolocation-!cn",
                        "github.com",
                        "githun.io",
                        "u9un.com",
                        "v2ray.com"
                    ],
                    "inboundTag": "auto",
                    "outboundTag": "fq"
                },
                {
                    "type": "field",
                    "ip": [
                        "geoip:cn"
                    ],
                    "inboundTag": "auto",
                    "outboundTag": "direct"
                },
                {
                    "type": "field",
                    "inboundTag": "auto",
                    "outboundTag": "direct"
                }
            ]
        },
    }
    c = config.ConfigObject.from_object(obj)
    assert c.to_object(ignore_none=True) == {
        'inbounds': [{'listen': '127.0.0.1',
                      'port': 1079,
                      'protocol': 'socks',
                      'settings': {'auth': 'noauth',
                                   'ip': '127.0.0.1',
                                   'udp': False,
                                   'userLevel': 0},
                      'tag': 'auto'},
                     {'listen': '127.0.0.1',
                      'port': 1080,
                      'protocol': 'socks',
                      'settings': {'auth': 'noauth',
                                   'ip': '127.0.0.1',
                                   'udp': False,
                                   'userLevel': 0},
                      'tag': 'fq'}],
        'log': {'access': '/var/log/v2ray/access.log',
                'error': '/var/log/v2ray/error.log',
                'loglevel': 'warn'},
        'outbounds': [{'protocol': 'freedom', 'settings': {}, 'tag': 'direct'},
                      {'protocol': 'blackhole', 'settings': {}, 'tag': 'blocked'},
                      {'protocol': 'vmess',
                       'settings': {
                           'vnext': [{'address': 'us1.top',
                                      'port': 80,
                                      'users': [{'alterId': 64,
                                                 'id': 'token',
                                                 'level': 0,
                                                 'security': 'auto'}]},
                                     {'address': 'us2.top',
                                      'port': 80,
                                      'users': [{'alterId': 64,
                                                 'id': 'token',
                                                 'level': 0,
                                                 'security': 'auto'}]}]},
                       'streamSettings': {'network': 'ws', 'security': 'none'},
                       'tag': 'fq'}],
        'routing': {'domainStrategy': 'AsIs',
                    'rules': [{'inboundTag': 'fq',
                               'outboundTag': 'fq',
                               'type': 'field'},
                              {'domain': ['geosite:geolocation-!cn',
                                          'github.com',
                                          'githun.io',
                                          'u9un.com',
                                          'v2ray.com'],
                               'inboundTag': 'auto',
                               'outboundTag': 'fq',
                               'type': 'field'},
                              {'inboundTag': 'auto',
                               'ip': ['geoip:cn'],
                               'outboundTag': 'direct',
                               'type': 'field'},
                              {'inboundTag': 'auto',
                               'outboundTag': 'direct',
                               'type': 'field'}]}}


if __name__ == '__main__':
    test_outbound_freedom()
    test_outbound_blackhole()
    test_inbound_vmess()
    test_inbound_socks()
    test_inbound_shadowsocks()
    test_inbound()
    test_outbound_vmess()
    test_outbound_socks()
    test_outbound_shadowsocks()
    test_outbound()

    test_routing_rule()
    test_routing_balancer()
    test_routing()

    test_config()
