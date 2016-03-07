from django import forms
from django.db import models
from django.utils.safestring import mark_safe

class CropImageMeta(type):
  def __new__(cls, *args, **kwargs):
    ncls = super(CropImageMeta, cls).__new__(cls, *args, **kwargs)
    if not hasattr(CropImageMeta, 'classes'):
      CropImageMeta.classes = {}
    CropImageMeta.classes[ncls.unique_name] = ncls
    return ncls

class CropImageWidget(forms.ClearableFileInput):

  def __init__(self, unique_name):
    self.unique_name = unique_name
    return super(CropImageWidget, self).__init__()

  def render(self, name, value, attrs=None):
    try:
      attrs['style'] = "display:none"
      Class = CropImageMeta.classes[self.unique_name]
      image_url = Class.get_image_url(value)
      clear_checkbox_name = self.clear_checkbox_name(name)
      html = "<img id=\"%s-img\" src=\"%s\" width=\"%spx\" height=\"%spx\" style=\"float:left\"><div style=\"float:left\">\
              <button type=\"button\" onclick=\"upload_image('%s',%s)\" style=\"float:left;margin:%spx 0 5px 10px\">\
              Upload Image</button><br><div style=\"float:left;margin-left:10px\">Clear:<input type=\"checkbox\" name=\"%s\"/></div></div>" % \
              (self.unique_name, image_url, Class.width, Class.height, self.unique_name,
               value.instance.pk, Class.height/2-23, clear_checkbox_name)
      return mark_safe(html)
    except Exception as e:
      del attrs['style']
      return super(CropImageWidget, self).render(name, value, attrs)

  class Media:
    js = (
      'jquery/jquery.min.js',
      'jquery/jquery-ui.min.js',
      'js/common.js',
      'js/crop_image/crop_image.js',
    )
    css = {'all':(
      'jquery/smoothness/jquery-ui.min.css',
      'jquery/custom.css',
    )}

class CropImageModelField(models.ImageField):
  def formfield(self, *args, **kwargs):
    kwargs.update({'widget': CropImageWidget(self.unique_name)})
    return super(models.ImageField, self).formfield(*args, **kwargs)

class CropImage(object):
  __metaclass__ = CropImageMeta

  unique_name = 'base_class'
  field_name = None
  width = None
  height = None

  @staticmethod
  def get_instance(request):
    pass

  @classmethod
  def FormField(cls, *args, **kwargs):
    kwargs['widget'] = CropImageWidget(cls.unique_name)
    return forms.ImageField(*args, **kwargs)

  @classmethod
  def ModelField(cls, *args, **kwargs):
    field = CropImageModelField(*args, **kwargs)
    field.unique_name = cls.unique_name
    return field
