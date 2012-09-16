# -*- coding: utf-8 -*-
from powerprompt.segments import library
import codecs
import os


class ColorBlock(object):
    BOLD = 1
    UNDERLINE = 4
    STRIKETHROUGH = 9

    def __init__(self, content, fg_color=None, bg_color=None,
                 left_padding=None, right_padding=None, attrs=()):
        self.content = content
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.left_padding = left_padding
        self.right_padding = right_padding
        self.attrs = attrs

    def set_defaults(self, fg_color=None, bg_color=None, left_padding=0,
                     right_padding=0):
        if self.fg_color is None:
            self.fg_color = fg_color
        if self.bg_color is None:
            self.bg_color = bg_color
        if self.left_padding is None:
            self.left_padding = left_padding
        if self.right_padding is None:
            self.right_padding = right_padding

    def render(self):
        output = ''
        if self.fg_color:
            output += '\\[\\e[38;5;%dm\\]' % (self.fg_color,)
        if self.bg_color:
            output += '\\[\\e[48;5;%dm\\]' % (self.bg_color,)
        for attr in self.attrs:
            output += '\\[\\e[%dm\\]' % (attr,)

        output += "%s%s%s" % (self.left_padding * ' ', self.content,
                              self.right_padding * ' ')
        return output + '\\[\\e[0m\\]'


class PowerPrompt(object):
    segment_dirs = (
        os.path.join(os.path.dirname(__file__), 'segments'),
        os.path.join(os.environ.get('HOME'), '.powerprompt', 'segments'),
    )

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        self.bg_color = settings.get('bg_color', 240)
        self.fg_color = settings.get('fg_color', 255)
        self.left_padding = settings.get('left_padding', 0)
        self.right_padding = settings.get('right_padding', 0)
        self.separator = codecs.encode(settings.get('separator', ''), 'utf-8')
        self.segments = settings.get('segments', [{
            'type': 'root',
        }])
        self.tail = settings.get('tail', '')

        for segment_dir in self.segment_dirs:
            if os.path.isdir(segment_dir):
                library.load_directory(segment_dir)

    def render(self):
        segments = []

        for segment in self.segments:
            config = segment.get('config', {})
            segment_cls = library.segments.get(segment.get('type'), None)
            if segment_cls is not None:
                segment_obj = segment_cls(config)
                if not segment_obj.is_usable():
                    continue
                segment_blocks = list(segment_obj.get_blocks())
                if len(segment_blocks) > 0:
                    segments.append(segment_blocks)

        output = ''
        for segment, next_segment in zip(segments, segments[1:] + [None]):
            for block in segment:
                block.set_defaults(self.fg_color, self.bg_color,
                                   self.left_padding, self.right_padding)
                output += block.render()
            if next_segment is not None:
                block = ColorBlock(self.separator, segment[-1].bg_color,
                                   next_segment[0].bg_color)
                block.set_defaults(self.fg_color, self.bg_color)
                output += block.render()
        if self.tail:
            tail = codecs.encode(self.tail, 'utf-8')
            block = ColorBlock(tail, fg_color=segments[-1][-1].bg_color)
            block.set_defaults(fg_color=self.bg_color)
            output += block.render()
        return output