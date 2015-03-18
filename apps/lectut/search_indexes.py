from haystack import indexes
from models import Post, Uploadedfile
#import datetime

class PostIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document = True,use_template = True)
  post = indexes.CharField(model_attr='content')
  user = indexes.CharField(model_attr='upload_user')

  def get_model(self):
    return Note

  def index_queryset(self, using=None):
    return Post.objects.all()

