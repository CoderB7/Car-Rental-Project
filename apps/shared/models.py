from uuid import uuid4
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
