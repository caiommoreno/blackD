from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    sex = models.CharField(max_length=6, blank=True, null=True)
    is_trial = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
   

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)       
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)
