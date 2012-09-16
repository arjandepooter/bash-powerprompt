# -*- coding: utf-8 -*-
from powerprompt.core import ColorBlock
from powerprompt.segments import BaseSegment
import os

class RootSegment(BaseSegment):
    name = 'root'

    def __init__(self, settings):
        super(RootSegment, self).__init__(settings)
        if os.environ.get('LAST_EXIT', '0') <> '0':
            self.bg_color = self.settings.get('bg_color_error', 160)
            self.fg_color = self.settings.get('fg_color_error', 255)

    def get_blocks(self):
        yield ColorBlock(codecs.encode(self.settings.get('text', '$'), 'utf-8'),
                         self.fg_color, self.bg_color)