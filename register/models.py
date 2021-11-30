from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Info(models.Model):
    bdate = models.DateField()
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    pin = models.CharField(max_length=6)
    state = models.CharField(max_length=20)
    profile_photo = models.ImageField(null=True, blank=True, upload_to='profile_photos/')
    document = models.FileField(null=True, blank=True,upload_to='profile_files/')
    user_id = models.ForeignKey(User, on_delete=CASCADE)