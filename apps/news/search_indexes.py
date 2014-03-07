
from haystack import indexes
from models import News
#import datetime

class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr = "item")

    def get_model(self):
      return News

    def index_queryset(self, using=None):
      return News.objects.all()


