from haystack import indexes
from models import Post, Uploadedfile
from nucleus.models import Faculty, Course
#import datetime

class PostIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document = True,use_template = True)
  post_id = indexes.CharField(model_attr='id')
  content = indexes.CharField(model_attr='content')
  content_auto = indexes.EdgeNgramField(model_attr='content')
#  user = indexes.CharField(model_attr='upload_user')

  def get_model(self):
    return Post

  def index_queryset(self, using=None):
    return Post.objects.all()


class FileIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document = True,use_template = True)
  image_id = indexes.CharField(model_attr='id')
  upload_file = indexes.CharField(model_attr='upload_file')
  description = indexes.CharField(model_attr='description')
  filename_auto = indexes.EdgeNgramField(model_attr='upload_file')
  description_auto = indexes.EdgeNgramField(model_attr='description')
#  file_type = indexes.CharField(model_attr='file_type')
#  upload_type = indexes.CharField(model_attr='upload_type')

  def get_model(self):
    return Uploadedfile

  def index_queryset(self, using=None):
    return Uploadedfile.objects.all()
