import json

from flighty.renderers import FlightyJSONRenderer


class TicketJSONRenderer(FlightyJSONRenderer):
    object_label = 'ticket'