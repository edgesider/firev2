import json
from base64 import b64decode
import requests

from ...json_data import json_data as j
from .base import BaseOutboundSettingObject, BaseInboundSettingObject


def _b64decode_pad(b64str):
    padsize = 3 - (len(b64str) + 3) % 4
    return b64decode(b64str + '=' * padsize)


# VmessOutbound
class VmessUserObject(j.JsonMap):
    _fields = [
        j.JsonMapField('id', str, constraint=j.F_REQUIRED),
        j.JsonMapField('alterId', int, constraint=j.F_REQUIRED),
        j.JsonMapField('security', str, constraint=j.F_REQUIRED),
        j.JsonMapField('level', int, constraint=j.F_REQUIRED),
    ]


class VmessUserArrayObject(j.JsonArray):

    @classmethod
    def _crt(cls, obj):
        return VmessUserObject.from_object(obj)


class VmessServerObject(j.JsonMap):
    _fields = [
        j.JsonMapField('address', str, constraint=j.F_REQUIRED),
        j.JsonMapField('port', int, constraint=j.F_REQUIRED),
        j.JsonMapField('users', VmessUserArrayObject, constraint=j.F_REQUIRED),
        j.JsonMapField('ps', str),
    ]

    @classmethod
    def from_vmess_str(cls, vmess):
        vmess = vmess.strip()
        vmess = vmess.replace('vmess://', '')
        conf = json.loads(_b64decode_pad(vmess))

        return cls.from_object({
            'address': conf['add'],
            'port': int(conf['port']),
            'users': [{
                'id': conf['id'],
                'alterId': int(conf['aid']),
                'security': 'auto',
                'level': 0
            }],
            'ps': conf['ps'],
        })


class VmessVnextArrayObject(j.JsonArray):

    @classmethod
    def _crt(cls, obj):
        return VmessServerObject.from_object(obj)

    def append_vnext(self, vnext: VmessServerObject):
        self._list.append(vnext)

    def append_from_vmess(self, vmess: str):
        self._list.append(VmessServerObject.from_vmess_str(vmess))


class VmessOutboundSettingObject(BaseOutboundSettingObject):
    _fields = [
        j.JsonMapField('vnext', VmessVnextArrayObject,
                       default=lambda: VmessVnextArrayObject.default(),
                       constraint=j.F_REQUIRED)
    ]

    @classmethod
    def create(cls, vstr):
        setting = cls.default()
        setting.vnext.append_from_vmess(vstr)
        return setting

    @classmethod
    def read_url(cls, url):
        """:return list of vmess str"""
        r = requests.get(url)
        r.encoding = 'ascii'
        return list(map(lambda x: x.strip(),
                        _b64decode_pad(r.text).decode('ascii').strip().split('\r\n')))


# VmessOutbound

# VmessInbound
class VmessClientObject(j.JsonMap):
    _fields = [
        j.JsonMapField('id', str, constraint=j.F_REQUIRED),
        j.JsonMapField('level', int, constraint=j.F_REQUIRED),
        j.JsonMapField('alterId', int, constraint=j.F_REQUIRED),
        j.JsonMapField('email', str, constraint=j.F_REQUIRED),
    ]


class VmessClientArrayObject(j.JsonArray):

    @classmethod
    def _crt(cls, obj):
        return VmessClientObject.from_object(obj)


class VmessDetourObject(j.JsonMap):
    _fields = [
        j.JsonMapField('to', str),
    ]


class VmessDefaultObject(j.JsonMap):
    _fields = [
        j.JsonMapField('level', int),
        j.JsonMapField('alterId', int),
    ]


class VmessInboundSettingObject(BaseInboundSettingObject):
    _fields = [
        j.JsonMapField('clients', VmessClientArrayObject, constraint=j.F_REQUIRED),
        j.JsonMapField('disableInsecureEncryption', bool),
        j.JsonMapField('default', VmessDefaultObject),
        j.JsonMapField('detour', VmessDetourObject)
    ]

# VmessInbound
