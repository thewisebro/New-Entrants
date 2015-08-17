from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from feeds.models import Feed, FeedTag


class ModelFeedMeta(type):
  modelfeeds = []
  def __new__(cls, *args, **kwargs):
    ncls = super(ModelFeedMeta, cls).__new__(cls, *args, **kwargs)
    if not ncls.__name__ == 'ModelFeed':
      modelfeed = ncls()
      model = modelfeed.Meta.model
      cls.modelfeeds.append(modelfeed)
      post_save.connect(modelfeed.on_save, sender=model)
      post_delete.connect(modelfeed.on_delete, sender=model)
    return ncls


class ModelFeed(object):
  __metaclass__ = ModelFeedMeta

  def add_tags(self, feed, tags):
    if tags:
      tag_instances = map(lambda (k,v):FeedTag.objects.get_or_create(key=k, value=v)[0], tags.items())
      feed.tags.add(*tag_instances)
      feed.save()

  def on_save(self, sender, **kwargs):
    instance = kwargs["instance"]
    instance_type = ContentType.objects.get_for_model(sender)
    if getattr(instance, 'trashed', None):
      self.delete_feed(instance.pk, instance_type)
      return
    created = kwargs["created"]
    app = self.Meta.app
    result = self.save(instance, created)
    if result == None:
      result = {}
    content = result.get('content', None)
    tags = result.get('tags', None)
    user = result.get('user', None)
    link = result.get('link', '')
    if content:
      if not Feed.objects.filter(instance_type=instance_type, instance_id=instance.id).exists():
        try:
          feed = Feed(app=app, instance_type=instance_type, instance_id=instance.id, content=content)
          feed.user = user
          feed.link = link
          feed.save()
          self.add_tags(feed, tags)
        except Exception as e:
          print "Exception : ",e
      else:
        feed = Feed.objects.get(instance_type=instance_type, instance_id=instance.id)
        feed.content = content
        feed.user = user
        feed.link = link
        feed.save()
        feed.tags.all().delete()
        self.add_tags(feed, tags)

  def delete_feed(self, instance_id, instance_type):
    try:
      feed = Feed.objects.get(instance_type=instance_type, instance_id=instance_id)
      feed.delete()
    except Feed.DoesNotExist:
      pass

  def on_delete(self, sender, **kwargs):
    if kwargs.has_key('instance'):
      instance = kwargs["instance"]
      instance_id = str(instance.pk)
    else:
      instance_id = kwargs['pk']
    instance_type = ContentType.objects.get_for_model(sender)
    self.delete(instance_id)
    self.delete_feed(instance_id, instance_type)

  def delete(self, instance_pk):
    pass

  @classmethod
  def mysql_trigger(self):
    assert self.Meta.php_app , "Not a php App"
    model = self.Meta.model
    table_name = model._meta.db_table
    pk_name = self.Meta.pk if hasattr(self.Meta,'pk') else model._meta.pk.name
    print \
"""DELIMITER |
CREATE TRIGGER """+table_name+"""_insert AFTER INSERT ON """+table_name+"""
  FOR EACH ROW BEGIN
    DECLARE cmd CHAR(255);
    DECLARE result CHAR(255);
    SET cmd = CONCAT('/home/feedsuser/channel-i/feeds/trigger.py INSERT """+table_name+""" ',NEW."""+pk_name+""");
    SET result =  sys_exec(cmd);
  END;
CREATE TRIGGER """+table_name+"""_update AFTER UPDATE ON """+table_name+"""
  FOR EACH ROW BEGIN
    DECLARE cmd CHAR(255);
    DECLARE result CHAR(255);
    SET cmd = CONCAT('/home/feedsuser/channel-i/feeds/trigger.py UPDATE """+table_name+""" ',NEW."""+pk_name+""");
    SET result =  sys_exec(cmd);
  END;
CREATE TRIGGER """+table_name+"""_delete BEFORE DELETE ON """+table_name+"""
  FOR EACH ROW BEGIN
    DECLARE cmd CHAR(255);
    DECLARE result CHAR(255);
    SET cmd = CONCAT('/home/feedsuser/channel-i/feeds/trigger.py DELETE """+table_name+""" ',OLD."""+pk_name+""");
    SET result =  sys_exec(cmd);
  END;
|
DELIMITER ;"""

