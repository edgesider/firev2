from ...json_data import json_data as j
from .base import BaseOutboundSettingObject, BaseInboundSettingObject


# outbound
class SocksUserObject(j.JsonMap):
    _fields = [
        j.JsonMapField('user', str),
        j.JsonMapField('pass', str),
        j.JsonMapField('level', int),
    ]


class SocksUserArrayObject(j.JsonArray):

    @classmethod
    def _crt(cls, obj):
        return SocksUserObject.from_object(obj)


class SocksServerObject(j.JsonMap):
    _fields = [
        j.JsonMapField('address', str, constraint=j.F_REQUIRED | j.F_NOTNULL),
        j.JsonMapField('port', str, constraint=j.F_REQUIRED | j.F_NOTNULL),
        j.JsonMapField('users', SocksUserArrayObject,
                       default=lambda: SocksUserArrayObject.default(),
                       constraint=j.F_REQUIRED | j.F_NOTNULL),
    ]


class SocksServerArrayObject(j.JsonArray):

    @classmethod
    def _crt(cls, obj):
        return SocksServerObject.from_object(obj)


class SocksOutboundSettingObject(BaseOutboundSettingObject):
    _fields = [
        j.JsonMapField('servers', SocksServerArrayObject,
                       default=lambda: SocksServerArrayObject.default(),
                       constraint=j.F_REQUIRED | j.F_NOTNULL)
    ]


# outbound

# inbound
class SocksAccountObject(j.JsonMap):
    _fields = [
        j.JsonMapField('user', str),
        j.JsonMapField('pass', str),
    ]


class SocksAccountArrayObject(j.JsonArray):

    @classmethod
    def _crt(cls, obj):
        return SocksAccountObject.from_object(obj)


class SocksInboundSettingObject(BaseInboundSettingObject):
    _fields = [
        j.JsonMapField('ip', str),
        j.JsonMapField('auth', str, default='noauth'),
        j.JsonMapField('accounts', SocksAccountArrayObject),
        j.JsonMapField('udp', bool),
        j.JsonMapField('userLevel', int),
    ]
# inbound
