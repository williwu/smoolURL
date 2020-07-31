from datetime import datetime
import random
import string
from .extensions import db

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(256))
    short_url = db.Column(db.String(20), unique=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # generate a random alias if no alias
        if len(self.short_url) == 0:
            self.short_url = self.generate_short_url()

    def generate_short_url(self):
        url = ("".join(random.choices(string.ascii_letters, k=5)))
        link = self.query.filter_by(short_url=url).first()

        if link:
            return self.generate_short_url()
        return url
