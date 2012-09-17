# -*- coding: utf-8 -*-
from powerprompt.core import ColorBlock
from powerprompt.segments import BaseSegment
import sh

class VcsSegment(BaseSegment):
    name = 'vcs'
    vcs_type = None

    def __init__(self, settings):
        super(VcsSegment, self).__init__(settings)
        self.fg_color_dirty = getattr(settings, 'fg_color_dirty', 239)
        self.bg_color_dirty = getattr(settings, 'bg_color_dirty', 208)

        vcs_types = {
            'svn': sh.svn.info,
            'git': sh.git.status,
            'hg': sh.hg.status,
        }
        for vcs_type, poll_command in vcs_types.iteritems():
            try:
                poll_command()
            except:
                pass
            else:
                self.vcs_type = vcs_type
                break

    def is_usable(self):
        return self.vcs_type is not None

    def get_git_status(self):
        states = sh.git.status('-s', '-b').stdout.split('\n')
        content = states[0][3:].strip()

        changes = {}
        for state in states[1:]:
            code = state[0:2].strip()
            if not code in changes:
                changes[code] = 0
            changes[code] += 1
        if '??' in changes:
            content += " +"

        dirty = len(changes) > 0
        return {
            'content': content,
            'fg_color': dirty and self.fg_color_dirty or self.fg_color,
            'bg_color': dirty and self.bg_color_dirty or self.bg_color,
        }

    def get_hg_status(self):
        content = sh.hg.branch(color=0).stdout.strip()
        states = sh.hg.status('-S', color=0).stdout.split('\n')

        dirty = len([s for s in states if len(s) > 0]) > 0
        if len([s for s in states if len(s) > 0 and s[0] == '?']) > 0:
            content += " +"

        return {
            'content': content,
            'fg_color': dirty and self.fg_color_dirty or self.fg_color,
            'bg_color': dirty and self.bg_color_dirty or self.bg_color,
        }

    def get_svn_status(self):
        info = dict([line.split(':', 1) for line in
                     sh.svn.info().stdout.split('\n') if ':' in line])

        path = info.get('URL', '').replace(info.get('Repository Root', ''), '')
        path_segments = path.split('/')[1:]
        if path_segments[0] in ('branches', 'tags'):
            content = path_segments[1]
        else:
            content = path_segments[0]

        states = sh.svn.status().strip().split('\n')
        dirty = len([s for s in states if len(s) > 0])
        if len([s for s in states if len(s) > 0 and s[0] == '?']) > 0:
            content += " +"

        return {
            'content': content,
            'fg_color': dirty and self.fg_color_dirty or self.fg_color,
            'bg_color': dirty and self.bg_color_dirty or self.bg_color,
        }

    def get_blocks(self):
        yield ColorBlock(**getattr(self, 'get_%s_status' % self.vcs_type,
                                 lambda: { 'content': 'error'})())