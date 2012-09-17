# -*- coding: utf-8 -*-
from powerprompt.core import ColorBlock
from powerprompt.segments import BaseSegment
import os

class UserSegment(BaseSegment):
    name = 'user'

    def is_usable(self):
        return 'USER' in os.environ

    def get_blocks(self):
        yield ColorBlock(os.environ.get('USER'), self.fg_color, self.bg_color,
                         attrs=(ColorBlock.BOLD,))