# -*- encoding: utf8 -*-
from __future__ import unicode_literals
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.encoders import JSONEncoder


class SafeJSONEncoder(JSONEncoder):
    def encode(self, o):
        # Override JSONEncoder.encode because it has hacks for
        # performance that make things more complicated.
        chunks = self.iterencode(o, True)
        if self.ensure_ascii:
            return ''.join(chunks)
        else:
            return u''.join(chunks)

    def iterencode(self, o, _one_shot=False):
        chunks = super(SafeJSONEncoder, self).iterencode(o, _one_shot)
        for chunk in chunks:
            chunk = chunk.replace('&', '\\u0026')
            chunk = chunk.replace('<', '\\u003c')
            chunk = chunk.replace('>', '\\u003e')
            yield chunk


class SafeJSONRenderer(JSONRenderer):
    encoder_class = SafeJSONEncoder
