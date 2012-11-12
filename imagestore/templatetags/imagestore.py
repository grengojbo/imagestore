# -*- mode: python; coding: utf-8; -*-
__author__ = 'jbo'
import logging
import re
import sys
from django.template import Library, Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str
from imagestore.models import Image

register = Library()
kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')
logger = logging.getLogger('imagestore')
class ImagestoreNodeBase(Node):
    """
    A Node that renders safely
    """
    nodelist_empty = NodeList()

    def render(self, context):
        try:
            return self._render(context)
        except Exception:
            #if settings.IMAGESTORE_DEBUG:
            #    raise
            logger.error('Imagestore tag failed:', exc_info=sys.exc_info())
            return self.nodelist_empty.render(context)

    def _render(self, context):
        raise NotImplemented()

class ImagestoreNode(ImagestoreNodeBase):
    child_nodelists = ('nodelist_file', 'nodelist_empty')
    error_msg = ('Syntax error. Expected: ``imagestore album limits '
                 '[key1=val1 key2=val2...] as var``')

    def __init__(self, parser, token):
        bits = token.split_contents()
        if len(bits) < 5 or bits[-2] != 'as':
            raise TemplateSyntaxError(self.error_msg)
        self.album_ = parser.compile_filter(bits[1])
        self.limits = parser.compile_filter(bits[2])
        self.options = []
        for bit in bits[3:-2]:
            m = kw_pat.match(bit)
            if not m:
                raise TemplateSyntaxError(self.error_msg)
            key = smart_str(m.group('key'))
            expr = parser.compile_filter(m.group('value'))
            self.options.append((key, expr))
        self.as_var = bits[-1]
        self.nodelist_file = parser.parse(('empty', 'endimagestore',))
        if parser.next_token().contents == 'empty':
            self.nodelist_empty = parser.parse(('endimagestore',))
            parser.delete_first_token()

    def _render(self, context):
        album_ = self.album_.resolve(context)
        limits = self.limits.resolve(context)
        options = {}
        for key, expr in self.options:
            noresolve = {u'True': True, u'False': False, u'None': None}
            value = noresolve.get(unicode(expr), expr.resolve(context))
            if key == 'options':
                options.update(value)
            else:
                options[key] = value
        #if settings.THUMBNAIL_DUMMY:
        #    thumbnail = DummyImageFile(geometry)
        #elif album_:
        if album_:
            thumbnail = Image.get_slider(album_, limits, **options)
        else:
            return self.nodelist_empty.render(context)
        context.push()
        context[self.as_var] = thumbnail
        output = self.nodelist_file.render(context)
        context.pop()
        return output

    def __repr__(self):
        return "<ImagestoreNode>"

    def __iter__(self):
        for node in self.nodelist_file:
            yield node
        for node in self.nodelist_empty:
            yield node


@register.tag
def imagestore(parser, token):
    return ImagestoreNode(parser, token)