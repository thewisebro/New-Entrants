from django.db import models

class Manager(models.Manager):
   def get_or_none(self, *args, **kwargs):
     try:
       return self.get(*args, **kwargs)
     except self.model.DoesNotExist:
       return None

class Model(models.Model):
  datetime_created = models.DateTimeField(auto_now_add=True)
  objects = Manager()

  class Meta:
    abstract = True
