from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
  phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
  # channel_name = models.CharField(max_length=17, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# class Module(models.Model):
#   user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#   pill_name = models.CharField(max_length=200)
#   module_num = models.IntegerField()

# class Scheduler(models.Model):
#   CATEGORY_CHOICES = (
#       ('w', 'week'),('d', 'day'), ('h', 'hour'), ('m', 'minute'), ('s', 'second'), ('o', 'once')
#     )

#   DAY_CHOICES = (
#       ('Mon', 'Monday'),
#       ('Tue', 'Tuesday'),
#       ('Wed', 'Wednesday'),
#       ('Thu', 'Thursday'),
#       ('Fri', 'Friday'),
#       ('Sat', 'Saturday'),
#       ('Sun', 'Sunday')
#     )

#   user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#   category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
#   day = models.CharField(max_length=3, choices=DAY_CHOICES, blank=True)
#   time_regex = RegexValidator(regex=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', message='HH:MM format')
#   time = models.CharField(validators=[time_regex], max_length=5, blank=True)
#   counter = models.IntegerField(blank=True)
#   module_nums = ArrayField(models.IntegerField())


