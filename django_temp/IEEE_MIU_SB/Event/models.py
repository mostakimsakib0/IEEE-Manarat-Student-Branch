from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    date = models.DateField()
    location = models.CharField(max_length=100)
    summary = models.TextField(max_length=200)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    description = CKEditor5Field("Text", config_name="extends")
    is_featured = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

