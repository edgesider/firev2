from collections.abc import Iterable

from ..json_data import json_data as j


class StringArrayObject(j.JsonArray):

    def __init__(self, *args):
        super().__init__()
        self._list = list(args)

    @classmethod
    def _crt(cls, obj):
        assert isinstance(obj, str)
        return obj


class SingleOrArrayStringObject(j.JsonCollection):
    '''
    既可以是单个字符串，也可以是字符串数组的对象
    '''

    @classmethod
    def from_object(cls, obj, parent=None):
        if isinstance(obj, str):
            return obj
        elif isinstance(obj, Iterable):
            return StringArrayObject.from_object(obj)
        raise ValueError(f'The first argument must be iterable or str')

    def to_object(self):
        raise NotImplementedError('Should not call the method here.')


class RuleObject(j.JsonMap):
    _fields = [
        j.JsonMapField('type', str, default='field'),
        j.JsonMapField('domain', StringArrayObject),
        j.JsonMapField('ip', StringArrayObject),
        j.JsonMapField('port', str),
        j.JsonMapField('source', StringArrayObject),
        j.JsonMapField('user', StringArrayObject),
        j.JsonMapField('inboundTag', SingleOrArrayStringObject),
        j.JsonMapField('protocol', StringArrayObject),
        j.JsonMapField('network', str),
        j.JsonMapField('attrs', str),
        j.JsonMapField('outboundTag', str),
        j.JsonMapField('balancerTag', str),
    ]


class RuleArrayObject(j.JsonArray):

    @classmethod
    def _crt(cls, obj):
        return RuleObject.from_object(obj)


class BalancerObject(j.JsonMap):
    _fields = [
        j.JsonMapField('tag', str),
        j.JsonMapField('selector', StringArrayObject),
    ]


class BalancerArrayObject(j.JsonArray):

    @classmethod
    def _crt(cls, obj):
        return BalancerObject.from_object(obj)


class RoutingObject(j.JsonMap):
    _fields = [
        j.JsonMapField('domainStrategy', str, default='AsIs'),
        j.JsonMapField('rules', RuleArrayObject,
                       default=lambda: RuleArrayObject.default()),
        j.JsonMapField('balancers', BalancerArrayObject, None)
    ]
