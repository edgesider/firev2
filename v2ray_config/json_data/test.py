import json_data as j


class TestMap_Default(j.JsonMap):
    _fields = [
        j.JsonMapField('value', str, default='default_value'),
        j.JsonMapField('callable', str, default=str),
    ]


if __name__ == '__main__':
    print(TestMap_Default.default().to_object())
