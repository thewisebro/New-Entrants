from django.db import models

class Manager(models.Manager):
  def get_or_none(self, *args, **kwargs):
    try:
      return self.get(*args, **kwargs)
    except self.model.DoesNotExist:
      return None

class ModelBase(models.base.ModelBase):
  def __new__(cls, *args, **kwargs):
    ncls = super(ModelBase, cls).__new__(cls, *args, **kwargs)
    if hasattr(ncls, 'post_save_receiver'):
      models.signals.post_save.connect(ncls.post_save_receiver, sender=ncls)
    return ncls

class Model(models.Model):
  datetime_created = models.DateTimeField(auto_now_add=True)
  objects = Manager()
  class Meta:
    abstract = True
