from ..json_data import json_data as j
from .protocol import (shadowsocks, socks,
                              vmess)


class InboundSettingFactory(j.JsonCollection):
    """
    Build an inbound-setting class from obj(dict).
    """

    @classmethod
    def from_object(cls, obj, parent=None):
        protocol = parent['protocol']
        if protocol == 'vmess':
            return vmess.VmessInboundSettingObject.from_object(obj)
        elif protocol == 'socks':
            return socks.SocksInboundSettingObject.from_object(obj)
        elif protocol == 'shadowsocks':
            return shadowsocks.ShadowsocksInboundSettingObject.from_object(obj)
        else:
            raise NotImplementedError(f'protocol `{protocol}` not supported')


class SockOptObject(j.JsonMap):
    _fields = [
        j.JsonMapField('mark', int),
        j.JsonMapField('tcpFastOpen', bool),
        j.JsonMapField('tproxy', str),
    ]


class StreamSettingsObject(j.JsonMap):
    _fields = [
        j.JsonMapField('network', str),
        j.JsonMapField('security', str),
        j.JsonMapField('sockopt', SockOptObject)
    ]


class SniffingDestOverrideObject(j.JsonArray):

    @classmethod
    def _crt(cls, obj):
        assert obj == 'http' or obj == 'tls'
        # TODO: Oneof
        return obj


class SniffingObject(j.JsonMap):
    _fields = [
        j.JsonMapField('enabled', bool),
        j.JsonMapField('destOverride', SniffingDestOverrideObject),
    ]


class AllocateObject(j.JsonMap):
    _fields = [
        j.JsonMapField('strategy', str),
        j.JsonMapField('refresh', int),
        j.JsonMapField('concurrency', int),
    ]


class InboundObject(j.JsonMap):
    _fields = [
        j.JsonMapField('tag', str,
                       constraint=j.F_REQUIRED | j.F_NOTNULL,
                       default=''),
        j.JsonMapField('protocol', str,
                       constraint=j.F_REQUIRED | j.F_NOTNULL,
                       default=''),
        j.JsonMapField('listen', str,
                       constraint=j.F_REQUIRED | j.F_NOTNULL,
                       default=''),
        j.JsonMapField('port', int,
                       constraint=j.F_REQUIRED | j.F_NOTNULL,
                       default=0),

        j.JsonMapField('settings', InboundSettingFactory),
        j.JsonMapField('streamSettings', StreamSettingsObject),
        j.JsonMapField('sniffing', SniffingObject),
        j.JsonMapField('allocate', str),
    ]


class InboundArrayObject(j.JsonArray):

    @classmethod
    def _crt(cls, obj):
        return InboundObject.from_object(obj)
