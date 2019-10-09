from ..json_data import json_data as j
from . import (inbound, outbound,
                     routing, log)


class ConfigObject(j.JsonMap):
    _fields = [
        j.JsonMapField('log', log.LogObject,
                       default=lambda: log.LogObject.default()),
        j.JsonMapField('routing', routing.RoutingObject,
                       default=lambda: routing.RoutingObject.default()),
        j.JsonMapField('inbounds', inbound.InboundArrayObject,
                       default=lambda: inbound.InboundArrayObject.default()),
        j.JsonMapField('outbounds', outbound.OutboundArrayObject,
                       default=lambda: outbound.OutboundArrayObject.default()),
    ]
