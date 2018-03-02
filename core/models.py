from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
  phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# class Medication(models.Model):
# 	pill_name = models.CharField(max_length=255)
# 	module_num = models.PositiveSmallIntegrerField()

class Medication(models.Model):
	pill_name = models.CharField(max_length=255)
	MODULE1 = '1'
	MODULE2 = '2'
	MODULE3 = '3'
	MODULE_CHOICES = (
		(MODULE1, 'Module 1'),
		(MODULE2, 'Module 2'),
		(MODULE3, 'Module 3'),
		)
	module_num = models.CharField(
		max_length=1,
		choices=MODULE_CHOICES,
		default=MODULE1,
		)

# class Schedule(models.Model):

