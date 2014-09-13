from core import models


class post(models.Model):
  text-content = models.TextField(blank=True)
  tags = models.ManyToManyField('FeedTag', blank=True, null=True)
  images=models.ManyToManyField('Image')
  post-date = models.DateTimeField(auto_now=True)

class FeedTag(models.Model):
  value = models.CharField(max_length=200)
  def __str__(self):
    return self.value

class Image(models.Model):



