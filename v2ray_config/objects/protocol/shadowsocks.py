from ...json_data import json_data as j
from .base import BaseOutboundSettingObject, BaseInboundSettingObject


# shadowsocks outbound
class ShadowsocksServerObject(j.JsonMap):
    _fields = [
        j.JsonMapField('address', str, default='127.0.0.1'),
        j.JsonMapField('port', int, default=0),
        j.JsonMapField('method', str),
        j.JsonMapField('password', str),
        j.JsonMapField('email', str),
        j.JsonMapField('ota', bool),
        j.JsonMapField('level', int),
    ]


class ShadowsocksServerArrayObject(j.JsonArray):

    @classmethod
    def _crt(cls, obj):
        return ShadowsocksServerObject.from_object(obj)


class ShadowsocksOutboundSettingObject(BaseOutboundSettingObject):
    _fields = [
        j.JsonMapField('servers', ShadowsocksServerArrayObject,
                       default=lambda: ShadowsocksServerArrayObject.default(),
                       constraint=j.F_REQUIRED | j.F_NOTNULL)
    ]


# shadowsocks outbound

# shadowsocks inbound
class ShadowsocksInboundSettingObject(BaseInboundSettingObject):
    _fields = [
        j.JsonMapField('method', str, constraint=j.F_REQUIRED | j.F_NOTNULL),
        j.JsonMapField('password', str),
        j.JsonMapField('email', str),
        j.JsonMapField('level', int),
        j.JsonMapField('ota', bool),
        j.JsonMapField('network', str, default='tcp'),
    ]
# shadowsocks inbound
