import os
import subprocess

from django.contrib.staticfiles.finders import BaseFinder
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils._os import safe_join

class HandlebarsFinder(BaseFinder):
  def __init__(self):
    self.root = safe_join(settings.STATIC_ROOT, 'HANDLEBARS_CACHE/')
    self.storage = FileSystemStorage(location=self.root)
    self.storage.prefix = ''
    self.file_name = 'templates.js'

  def find(self, path, all=False):
    if path.endswith(self.file_name):
      dir_path = path[:-len(self.file_name)]
      app = '_'.join(filter(lambda x:x, dir_path.split('/')[1:]))
      if app:
        namespace = 'Handlebars.' + app + '_templates'
      else:
        namespace = 'Handlebars.templates'
      cache_path = safe_join(self.root, dir_path)
      template_path = safe_join(cache_path, self.file_name)
      for STATIC_PATH in settings.STATICFILES_DIRS:
        source_path = safe_join(STATIC_PATH, dir_path)
        if os.path.exists(source_path):
          if not os.path.exists(cache_path):
            os.makedirs(cache_path)
          if not os.path.exists(template_path) or\
              os.path.getmtime(template_path) < os.path.getmtime(source_path):
            command = ['handlebars', '-m', '-e', 'hbs', '-n', namespace,
              source_path, '-f', template_path]
            subprocess.call(command)
          return template_path
    return []

  def list(self, ignore_patterns):
    for STATIC_PATH in settings.STATICFILES_DIRS:
      for root, dirs, files in os.walk(STATIC_PATH):
        handlebars_files = False
        for f in files:
          if f.endswith('.hbs'):
            handlebars_files = True
            break
        if handlebars_files:
          path = safe_join(root, self.file_name)
          path = path.split(STATIC_PATH)[1][1:]
          # create cache
          self.find(path)
    for root, dirs, files in os.walk(self.root):
      for f in files:
        if f == self.file_name:
          path = safe_join(root, f)
          path = path.split(self.root)[1][1:]
          yield path, self.storage
