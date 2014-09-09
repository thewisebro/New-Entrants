from core import models
from nucleus.models import User

"""
def store_default_pref(newsuser, channel):
    channel_pref = ChannelPref(channel=channel, newsuser=newsuser)
    channel_pref.save()
"""

class NewsUser(models.Model):
  user = models.OneToOneField(User)
  channel_pref = models.ManyToManyField('Channel', through='ChannelPref')
  source_pref = models.ManyToManyField('Source', through='SourcePref')

  def __unicode__(self):
    return self.user.username
  """
  def save(self):
    map(lambda c: (store_default_pref(self, c)), Channel.objects.all())
    super(NewsUser, self).save()
  """

class News(models.Model):
  title = models.CharField(max_length=120)
  description_text = models.TextField()
  image_path = models.CharField(max_length=100)
  item = models.TextField()
  article_date = models.DateTimeField()
  channel = models.ForeignKey('Channel')
  source = models.ForeignKey('Source')
  views = models.IntegerField(max_length=4, default=0)
  is_active = models.BooleanField(default=True)

  def __unicode__(self):
     return self.title

class Channel(models.Model):
  name = models.CharField(max_length=20)
  sources = models.ManyToManyField('Source')

  def __unicode__(self):
    return self.name

class Source(models.Model):
  name = models.CharField(max_length=20)
  default_banner = models.ImageField(upload_to = 'news/banners/')
  #read_status = models.ManyToManyField('NewsUser', through='ReadStatus')

  def __unicode__(self):
    return self.name

class ChannelPref(models.Model):
  newsuser = models.ForeignKey('NewsUser')
  channel = models.ForeignKey('Channel')
  pref_value = models.IntegerField(max_length=3, default=100)
  #pref_status = models.BooleanField(default=True)
  #pref_order = models.IntegerField(max_length=2, default=0)

class SourcePref(models.Model):
  newsuser = models.ForeignKey('NewsUser')
  source = models.ForeignKey('Source')
  channel = models.ForeignKey('Channel')
  pref_value = models.IntegerField(max_length=3, default=100)


"""
class ReadStatus(models.Model):
  user = models.ForeignKey('NewsUser')
  channel = models.ForeignKey('Source')
  is_read = models.BooleanField(default=False)
"""



"""
class related_news(models.Model):
  item = models.ManyToManyField(news_feeds)
  main_item = models.ForeignKey(news_feeds, related_name="main_items")
  related_items = models.ForeignKey(news_feeds, related_name="related_names")
"""
