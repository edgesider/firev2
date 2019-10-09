import json
from base64 import b64decode

import requests

from ..json_data import json_data as j
from .protocol import (blackhole, freedom, vmess,
                              shadowsocks, socks)
from .protocol.base import BaseOutboundSettingObject


def _b64decode_pad(b64str):
    padsize = 3 - (len(b64str) + 3) % 4
    return b64decode(b64str + '=' * padsize)


class OutboundSettingFactory(j.JsonCollection):
    """
    Build an outbound-setting class from obj(dict).
    """

    @classmethod
    def from_object(cls, obj, parent=None):
        protocol = parent['protocol']
        if protocol == 'vmess':
            return vmess.VmessOutboundSettingObject.from_object(obj)
        elif protocol == 'blackhole':
            return blackhole.BlackholeOutboundSettingObject.from_object(obj)
        elif protocol == 'freedom':
            return freedom.FreedomOutboundSettingObject.from_object(obj)
        elif protocol == 'shadowsocks':
            return shadowsocks.ShadowsocksOutboundSettingObject.from_object(obj)
        elif protocol == 'socks':
            return socks.SocksOutboundSettingObject.from_object(obj)
        else:
            raise NotImplementedError(f'protocol `{protocol}` not supported')


class SockoptObject(j.JsonMap):
    _fields = [
        j.JsonMapField('mark', int),
        j.JsonMapField('tcpFastOpen', bool),
        j.JsonMapField('tproxy', str),
    ]


class StreamSettingsObject(j.JsonMap):
    _fields = [
        j.JsonMapField('network', str),
        j.JsonMapField('security', str),
        j.JsonMapField('sockopt', SockoptObject)
    ]

    @classmethod
    def create(cls, **kwargs):
        vstr = kwargs.get('vstr')

        vstr = vstr.strip()
        vstr = vstr[len('vmess://'):]
        conf = json.loads(_b64decode_pad(vstr))
        obj = cls.default()
        obj.network = conf['net']
        tls = conf.get('tls')
        if tls: # not empty string and not None
            obj.security = tls
        return obj


class ProxySettingsObject(j.JsonMap):
    _fields = [
        j.JsonMapField('tag', str)
    ]


class MuxSettingsObject(j.JsonMap):
    _fields = [
        j.JsonMapField('enabled', bool),
        j.JsonMapField('concurrency', int)
    ]


class OutboundObject(j.JsonMap):
    _fields = [
        j.JsonMapField('tag', str,
                       constraint=j.F_REQUIRED,
                       default=''),
        j.JsonMapField('protocol', str,
                       constraint=j.F_REQUIRED,
                       default=''),
        j.JsonMapField('settings', OutboundSettingFactory),
        j.JsonMapField('streamSettings', StreamSettingsObject),
        j.JsonMapField('proxySettings', ProxySettingsObject),
        j.JsonMapField('sendThrough', str),
    ]

    @classmethod
    def create(cls, protocol, tag, **create_arg):
        if protocol == "vmess":
            # setting = vmess.VmessOutboundSettingObject.create(**create_arg)
            return cls.create_vmess(tag, **create_arg)
        else:
            raise NotImplementedError(f'protocol `{protocol}` not supported')

    @classmethod
    def create_vmess(cls, tag, **create_arg):
        """If `vmess` is given, return only one VmessOutbound.
        Else if `url` is given, return list of VmessOutbound
        whose `vnext` has only one node or one VmessOutbound
        whose `vnext` has list of node, depended on `gen_list` argument."""
        url = create_arg.get('url')
        vstr = create_arg.get('vmess')
        gen_list = create_arg.get('gen_list')

        if vstr is not None:
            setting = vmess.VmessOutboundSettingObject.create(vstr=vstr)
            outbound = cls.default()
            outbound.protocol = 'vmess'
            outbound.tag = tag
            outbound.settings = setting
            outbound.streamSettings = None
        elif url is not None:
            vstr_list = cls.read_vmess_url(url)
            if not gen_list:
                setting = vmess.VmessOutboundSettingObject.default()
                for v in vstr_list:
                    setting.vnext.append_from_vmess(v)
                stream = StreamSettingsObject.create(vstr=vstr_list[0])
                outbound = cls.default()
                outbound.protocol = 'vmess'
                outbound.tag = tag
                outbound.settings = setting
                outbound.streamSettings = stream
            else:
                outbound = []
                for v in vstr_list:
                    out = cls.default()
                    out.protocol = 'vmess'
                    out.tag = tag
                    out.settings = vmess.VmessOutboundSettingObject.create(vstr=v)
                    out.streamSettings = StreamSettingsObject.create(vstr=v)
                    outbound.append(out)
        else:
            raise Exception('Both vmess and url is None')

        return outbound

    @classmethod
    def read_vmess_url(cls, url):
        """:return list of vmess str"""
        r = requests.get(url)
        r.encoding = 'ascii'
        s: str = cls._b64decode_pad(r.text).decode('ascii').strip()
        if s.find('\n') > s.find('\r\n'):
            split = '\n'
        else:
            split = '\r\n'
        return list(map(lambda x: x.strip(),
                        s.split(split)))

    @staticmethod
    def _b64decode_pad(b64str):
        padsize = 3 - (len(b64str) + 3) % 4
        return b64decode(b64str + '=' * padsize)

    def __setattr__(self, key, value):
        if key == 'settings':
            setting = value

            if setting is None:
                super().__setattr__('settings', setting)
                return

            if not isinstance(setting, BaseOutboundSettingObject):
                raise ValueError(f'unexpect type `{type(setting).__name__}`, '
                                 f'must be `{BaseOutboundSettingObject.__name__}`')
            super().__setattr__('settings', setting)

            if isinstance(setting, vmess.VmessOutboundSettingObject):
                self.protocol = 'vmess'
            elif isinstance(setting, socks.SocksOutboundSettingObject):
                self.protocol = 'socks'
        else:
            super().__setattr__(key, value)


class OutboundArrayObject(j.JsonArray):

    @classmethod
    def _crt(cls, obj):
        return OutboundObject.from_object(obj)

    def add_vmess(self, vmess_str):
        pass
