import os
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from shop.models import Shop

class Place(models.Model):
  title = models.CharField(max_length = 255)
  description = models.TextField(blank=True)
  image = models.ImageField(upload_to='place', blank=True)
  externalURL = models.URLField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  shop = models.ForeignKey(Shop, related_name='places', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
  phone_number = models.CharField(max_length = 255, default='', blank=True)
  email = models.CharField(max_length = 255, default='', blank=True)

  def url(self):
      # returns a URL for either internal stored or external image url
      if self.externalURL:
          return self.externalURL
      else:
          return os.path.join('/', settings.MEDIA_URL, 'place/', os.path.basename(str(self.image)))

  def image_tag(self):
      return mark_safe('<img src="{src}" width="{width}" height="{height}" />'.format(
                src=self.url(), 
                width=150,
                height=(150/self.image.width * self.image.height) 
            ))

  image_tag.short_description = 'Image'    

  def __str__(self):
    return self.title