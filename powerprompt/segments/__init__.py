# -*- coding: utf-8 -*-
import imp
import os


class Library(object):
    def __init__(self):
        self.segments = {}

    def register(self, klass):
        self.segments[klass.name] = klass

    def load_directory(self, directory):
        for sub in os.listdir(directory):
            path = os.path.join(directory, sub)
            if os.path.isfile(path) and path.endswith('.py'):
                imp.load_source('segment', path)
library = Library()


class SegmentMeta(type):
    def __init__(cls, name, bases, dct):
        if cls.__name__ <> 'BaseSegment':
            library.register(cls)


class BaseSegment(object):
    __metaclass__ = SegmentMeta
    name = '_base_'

    def __init__(self, settings):
        self.fg_color = settings.get('fg_color')
        self.bg_color = settings.get('bg_color')
        self.settings = settings

    def is_usable(self):
        return True

    def get_blocks(self):
        raise NotImplementedError()