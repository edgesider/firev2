from ..json_data import json_data as j


class LogObject(j.JsonMap):
    _fields = [
        j.JsonMapField('access', str, default='./access.log'),
        j.JsonMapField('error', str, default='./error.log'),
        j.JsonMapField('loglevel', str, default='warn'),
    ]
