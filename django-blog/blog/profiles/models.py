from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from blogApp.models import Post

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post,null=True,blank=True, on_delete=models.CASCADE)
	description = models.CharField(max_length=500, default='')
	email = models.EmailField(null=True,blank=True)
	image = models.ImageField(upload_to='profile_image', blank=True)

	def __str__(self):
		return self.user.username

def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
