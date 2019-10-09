from ...json_data import json_data as j
from .base import BaseOutboundSettingObject


# FreedomOutbound
class FreedomOutboundSettingObject(BaseOutboundSettingObject):
    _fields = [
        j.JsonMapField('domainStrategy', str),
        j.JsonMapField('redirect', str),
        j.JsonMapField('user_level', str),
    ]

# FreedomOutbound
