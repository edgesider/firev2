from collections.abc import Iterable

__all__ = [
    'JsonCollection',
    'JsonArray',
    'JsonMap',
    'JsonMapField',

    'F_REQUIRED',
    'F_NOTNULL',
]

'The field must exist.'
F_REQUIRED = 1
'The field should not be null if it exists.'
F_NOTNULL = 2


class JsonCollection():

    @classmethod
    def default(cls):
        raise NotImplementedError()

    @classmethod
    def from_object(cls, obj, parent=None):
        raise NotImplementedError()

    def to_object(cls, *args, **kwargs):
        raise NotImplementedError()


class JsonArray(JsonCollection):
    _crt = lambda o: o

    def __init__(self):
        self._list = []

    @classmethod
    def default(cls):
        return cls()

    @classmethod
    def from_object(cls, arr, parent=None):
        obj = cls()
        assert isinstance(arr, Iterable)

        for entry in arr:
            obj._list.append(cls._crt(entry))
        return obj

    def to_object(self, *args, **kwargs):
        l = []
        for val in self._list:
            if isinstance(val, JsonCollection):
                val = val.to_object(*args, **kwargs)
            l.append(val)
        return l

    def find_one(self, func):
        for obj in self._list:
            if func(obj):
                return obj
        return None

    def find_all(self, func):
        l = []
        for obj in self._list:
            if func(obj):
                l.append(obj)
        return l if l else None

    def delete_one(self, func):
        for i, obj in enumerate(self._list):
            if func(obj):
                return self._list.pop(i)
        return None

    def insert(self, idx, obj):
        self._list.insert(idx, obj)

    def append(self, o):
        self._list.append(o)

    def __iter__(self):
        return self._list.__iter__()

    def __repr__(self):
        return self._list.__repr__()

    def __str__(self):
        return self._list.__str__()

    def __getitem__(self, *arg):
        return self._list.__getitem__(*arg)


def _key2attr(key_name: str):
    return str(key_name)


class JsonMapField:
    """
    `obj_name`: Attribute name in the object.
    `key_name`: The key in dict.
    `constructor`: A callable can constructor an object from a dict.
    `constraint`: Field's constraint(s).
    """

    def __init__(self, key_name, constructor,
                 constraint=None, attr_name=None, default=None):
        if attr_name is None:
            attr_name = _key2attr(key_name)
        self._attr_name = attr_name
        self._key_name = key_name
        self._constructor = constructor
        self._constraint = constraint
        self._default = default

    @property
    def attr_name(self):
        return self._attr_name

    @property
    def key_name(self):
        return self._key_name

    @property
    def constructor(self):
        return self._constructor

    @property
    def constraint(self):
        return self._constraint

    @property
    def default(self):
        """Default value.
        Valid in `JsonMap.default` and `JsonMap.from_object`."""
        o = self._default
        return o() if callable(o) else o

    # TODO 字段有效性检查


class JsonMap(JsonCollection):
    '''
    Every field has its constructor.
    '''

    _fields = []

    @classmethod
    def default(cls):
        obj = cls()
        for field in cls._fields:
            setattr(obj, field.attr_name, field.default)
        return obj

    @classmethod
    def from_object(cls, d, parent=None):
        if d is None:
            return None
        obj = cls()
        for field in cls._fields:
            crt = field.constructor
            constraint = field.constraint
            key_name = field.key_name
            attr_name = field.attr_name
            value = d.get(key_name)

            # field check
            if constraint is not None:
                if constraint & F_REQUIRED and \
                        key_name not in d:
                    raise KeyError(f'field <{field.key_name}> is required in <{cls.__name__}>.')
                if constraint & F_NOTNULL and \
                        key_name in d and value is None:
                    raise KeyError(f'field <{field.key_name}> should not be null in <{cls.__name__}>.')

            # check passed
            if key_name not in d:
                value = field.default

            if value is not None:
                if issubclass(crt, JsonCollection):
                    value = crt.from_object(value, d)
                else:
                    value = crt(value)
            setattr(obj, attr_name, value)
        return obj

    def to_object(self, *args, **kwargs):
        ignore_none = kwargs.get('ignore_none', False)
        d = {}
        for field in self._fields:
            key_name = field.key_name
            attr_name = field.attr_name
            value = getattr(self, attr_name)

            if isinstance(value, JsonCollection):
                value = value.to_object(*args, **kwargs)
            if ignore_none and value is None:
                continue
            d[key_name] = value

        return d
