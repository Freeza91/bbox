import os
import json
import sys
from .utils import json_dumps

local = None
def parse_local():
    global local
    if local is None:
        config_path = os.path.join(os.getcwd(),
                                   'tup.config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            local = json.load(f)
        # validaty
        assert local['port_range'][0] < local['port_range'][1]
    return local

class GrandConfig:
    def __init__(self):
        self.sections = {}

    def set(self, sec, key, value):
        section = self.sections.setdefault(sec, {})
        section[key] = value

    def delete(self, sec, key):
        section = self.sections.get(sec)
        if section:
            return section.pop(key, None)

    def delete_section(self, sec):
        return self.sections.pop(sec, None)
        
    def get(self, sec, key, default=None):
        section = self.sections.get(sec)
        if section:
            return section.get(key, default)

    def get_strict(self, sec, key):
        return self.sections[sec][key]

    def get_section(self, sec):
        return self.sections.get(sec)

    def get_section_strict(self, sec):
        return self.sections[sec]
    
    def has_section(self, sec):
        return sec in self.sections

    def has_key(self, sec, key):
        return (self.has_section(sec) and
                key in self.sections[sec])
    
    def items(self, sec):
        return self.sections[sec].items()

    def triple_items(self):
        for sec, section in sorted(self.sections.items()):
            for key, value in sorted(section.items()):
                yield sec, key, value

    def clear(self):
        self.sections = {}

    def dump_json(self):
        return json_dumps(self.sections)

grand = GrandConfig()
