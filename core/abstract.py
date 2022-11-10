_B=False
_A=True
import uuid
from django.db import models
class BaseAbstractModel(models.Model):
	id=models.BigAutoField(primary_key=_A,editable=_B);uuid=models.UUIDField(unique=_A,default=uuid.uuid4,editable=_B);created_at=models.DateTimeField(auto_now_add=_A,editable=_B);updated_at=models.DateTimeField(auto_now=_A,editable=_B)
	class Meta:app_label='core';abstract=_A;ordering=['-updated_at']