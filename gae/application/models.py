# raku-tabi application/models.py

import re
import time

from tools import db


def utc_now():
    return int(time.time())


class Keyword3(db.Model):
    """ self.key = kind + name(str) """

    created = db.Property('c', default=utc_now())

    @property
    def word(self):
        return self.key.name

    @property
    def path(self):
        return "/".join(self.word.split())

'''
class Item3(db.Model):
    """ self.key = kind + name(str) """

    keywords = db.Property('w', default=dict())
    created = db.Property('c', default=utc_now())

    @property
    def short_name(self):
        return self.name[:30] if hasattr(self, 'name') else None

    @property
    def description(self):
        return (re.sub(re.compile(r'<.*?>'), "", self.caption)[:120]
                if hasattr(self, 'caption') else None)

    @property
    def links(self):
        return ([Keyword(keyword) for keyword in self.keywords]
                if self.keywords else None)
'''


