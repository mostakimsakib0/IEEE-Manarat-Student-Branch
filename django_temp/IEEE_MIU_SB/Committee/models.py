from django.db import models
from django.contrib.auth.models import User
from Committee.constants import DESIGNATION_CHOICES, gender_choices
from django.utils.text import slugify

class WebDetails(models.Model):
    viewer_count = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"Web Details - Viewer Count: {self.viewer_count}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    gender = models.CharField(max_length=10, choices=gender_choices)
    designation = models.IntegerField(choices=DESIGNATION_CHOICES)
    session = models.ForeignKey("Session", on_delete=models.CASCADE)
    facebook_profile = models.URLField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    is_valid = models.BooleanField(default=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    class Meta:
        ordering = ["timestamp"]

class Session(models.Model):
    year = models.CharField(max_length=10)
    slug = models.SlugField(max_length=100, unique=True) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.year)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.year
