from marshmallow.fields import Nested
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class SmartNested(Nested):
    def serialize(self, attr, obj, accessor=None):
        if attr not in obj.__dict__:
            return (getattr(obj, attr + "_id"))
        return super(SmartNested, self).serialize(attr, obj, accessor)