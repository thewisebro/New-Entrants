from core import models


class post(models.Model):
  text_content = models.CharField(max_length=200)
# tags = models.ManyToManyField('FeedTag', blank=True, null=True)
 # images=models.ManyToManyField('Image')
  post_date = models.DateTimeField(auto_now=True)

#class FeedTag(models.Model):
# value = models.CharField(max_length=200)
# def __str__(self):
#   return self.value





