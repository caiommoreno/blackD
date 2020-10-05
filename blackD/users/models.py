from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    jobAs = models.OneToOneField(Job, on_delete=models.SET_NULL, null=True, blank=True)
    balance = models.IntegerField(default=0, blank=True, null=True)
    sex = models.CharField(max_length=6, blank=True, null=True)
    last_logout = models.DateField(default='1970-01-01', blank=True, null=True)
    staff_requested = models.BooleanField(default=False)
    work = models.CharField(max_length=999, blank=True, null=True)
    is_team = models.BooleanField(default=False)
   

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
