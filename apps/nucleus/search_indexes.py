from haystack import indexes
from models import Course, User

class CourseIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document = True,use_template = True)
  code = indexes.CharField(model_attr='code')
  name = indexes.CharField(model_attr='name')
  code_auto = indexes.EdgeNgramField(model_attr='code')
  name_auto = indexes.EdgeNgramField(model_attr='name')

  def get_model(self):
    return Course

  def index_queryset(self, using=None):
    return Course.objects.all()


class UserIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document = True,use_template = True)
  name = indexes.CharField(model_attr='name')
  name_auto = indexes.EdgeNgramField(model_attr='name')

  def get_model(self):
    return User

  def index_queryset(self, using=None):
    return User.objects.all()
