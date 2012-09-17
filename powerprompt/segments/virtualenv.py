# -*- coding: utf-8 -*-
from powerprompt.core import ColorBlock
from powerprompt.segments import BaseSegment
import os

class VirtualenvSegment(BaseSegment):
    name = 'virtualenv'

    def is_usable(self):
        return 'VIRTUAL_ENV' in os.environ

    def get_blocks(self):
        virtualenv = os.path.basename(os.environ['VIRTUAL_ENV'])
        yield ColorBlock(virtualenv, self.fg_color, self.bg_color)