from django.db import models

class ModelWithTimeStamp(models.Model):
    """ safely adds create_at field to any model that inherits this """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
