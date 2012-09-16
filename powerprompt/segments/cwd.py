# -*- coding: utf-8 -*-
from powerprompt.core import ColorBlock
from powerprompt.segments import BaseSegment
import os

class CwdSegment(BaseSegment):
    name = 'cwd'

    def __init__(self, settings):
        super(CwdSegment, self).__init__(settings)
        self.path_seperator = settings.get('path_seperator', '⮁')
        self.max_left = settings.get('max_left', 2)
        self.max_right = settings.get('max_right', 2)

    def get_blocks(self):
        path = os.path.realpath(os.path.curdir)
        home_dir = os.environ.get('HOME', '')
        if path.startswith(home_dir):
            path = path.replace(home_dir, '~')
        if path.startswith('/'):
            path = path[1:]
        path_segments = path.split('/')

        if self.max_left > 0 and self.max_right > 0 and \
           len(path_segments) > self.max_left + self.max_right:
            path_segments = path_segments[:self.max_left] + ["..."] + path_segments[-self.max_right:]

        for i, path_segment in enumerate(path_segments, 1):
            if i <> len(path_segments):
                yield ColorBlock(path_segment, self.fg_color, self.bg_color)
                yield ColorBlock(self.path_seperator, self.fg_color,
                                 self.bg_color, 0, 0)
            else:
                yield ColorBlock(path_segment, self.fg_color, self.bg_color,
                                 attrs=(ColorBlock.BOLD,))