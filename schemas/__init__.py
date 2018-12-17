from marshmallow import Schema, post_load

class EmbeddingSchema(Schema):
    accessData = {}
    
    @post_load
    def mask_data(self, data):
        maskedAccessData = {}
        for key in data:
            if data[key]:
                maskedAccessData[key] = self.accessData[key]
        return maskedAccessData