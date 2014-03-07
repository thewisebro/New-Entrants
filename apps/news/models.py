from core import models

class News(models.Model):
  title = models.CharField(max_length=120)
  description_text = models.TextField()
  image_path = models.CharField(max_length=100)
  item = models.TextField()
  article_date = models.DateTimeField()
  channel = models.CharField(max_length=20)
  source = models.CharField(max_length=30)

  def __unicode__(self):
     return self.title
'''
class related_news(models.Model):
  item = models.ManyToManyField(news_feeds)
  main_item = models.ForeignKey(news_feeds, related_name="main_items")
  related_items = models.ForeignKey(news_feeds, related_name="related_names") '''
