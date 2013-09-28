from django.http import HttpResponse
from django.shortcuts import render

from base import CropImageMeta
from forms import PhotoForm

import os
from PIL import Image

def upload_image(request, unique_name, pk):
  Class = CropImageMeta.classes[unique_name]
  instance = Class.get_instance(request, pk)
  image_field = getattr(instance, Class.field_name)
  image_url = Class.get_image_url(image_field)

  photoform = PhotoForm()
  if request.method == 'POST':
    crop = False
    if request.POST.has_key('upload'):
      cropping_done = False
      if int(request.POST['is_ie']):
        cropping_done = True
      photoform = PhotoForm(request.POST, request.FILES)
      if photoform.is_valid():
        save_count = 0
        if image_field and os.path.exists(image_field.path):
          filename = save_count = image_field.name.split('/')[-1].split('.')[0]
          if len(filename.split('_')) > 1:
            save_count = int(filename.split('_')[-1]) + 1
        if image_field:
          if os.path.exists(image_field.path):
            os.remove(image_field.path)
          image_field.delete()
        f = request.FILES['photo']
        fname = request.user.username + '_' + str(save_count) + '.' + f.name.split('.')[-1]
        image_field.save(fname,f,save=True)
        image_url = Class.get_image_url(image_field)
        crop = True
      return render(request, 'crop_image/upload_image.html', {
                    'photoform': photoform,
                    'crop': crop,
                    'image_url': image_url,
                    'cropping_done': cropping_done,
                    'cropimageclass': Class
                  })
    else:
      try:
        x = int(float(request.POST['x'][:7]))
        y = int(float(request.POST['y'][:7]))
        w = int(float(request.POST['w'][:7]))
        h = int(float(request.POST['h'][:7]))
        im = Image.open(image_field.path)
        width,height = im.size
        rx = int(x * width / 400.0)
        ry = int(y * width / 400.0)
        rw = int(w * width / 400.0)
        rh = int(h * width / 400.0)
        if rx+rw > width:
          rw = width - rx
        if ry+rh > height:
          rh = height - ry
        img = im.crop((rx,ry,rx + rw,ry + rh))
        img.thumbnail((Class.width, Class.height), Image.ANTIALIAS)
        img.save(image_field.path, quality=100)
        return render(request, 'crop_image/upload_image.html', {
                      'photoform': photoform,
                      'cropping_done': True,
                      'crop': True,
                      'image_url': image_url,
                      'cropimageclass': Class
                    })
      except Exception as e:
        return render(request, 'crop_image/upload_image.html',{
                      'photoform': photoform,
                      'crop': True,
                      'image_url': image_url,
                      'cropping_done': False,
                      'cropimageclass': Class
                    })

  return render(request, 'crop_image/upload_image.html', {
                'photoform': photoform,
                'image_url': image_url,
                'cropimageclass': Class
              })
