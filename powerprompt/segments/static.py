# -*- coding: utf-8 -*-
from powerprompt.core import ColorBlock
from powerprompt.segments import BaseSegment
import codecs

class StaticSegment(BaseSegment):
    name = 'static'

    def is_usable(self):
        return len(self.settings.get('text', '')) > 0

    def get_blocks(self):
        yield ColorBlock(codecs.encode(self.settings.get('text'), 'utf-8'),
                         self.fg_color, self.bg_color)