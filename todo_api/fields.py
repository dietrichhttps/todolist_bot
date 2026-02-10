from django.db import models
import uuid
import hashlib

class CustomAutoField(models.BigAutoField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname, None):
            pk_value = self.generate_pk()
            setattr(model_instance, self.attname, pk_value)
            return pk_value
        else:
            return super().pre_save(model_instance, add)
    
    def generate_pk(self):
        timestamp = str(uuid.uuid1().int >> 64)
        random_part = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:8]
        return int(timestamp + random_part, 16)