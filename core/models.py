from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

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

class Schedule(models.Model):
	# CONFIRM THESE CATEGORIES
	SECOND = datetime.timedelta(seconds=1)
	MINUTE = datetime.timedelta(minutes=1)
	HOURLY = datetime.timedelta(hours=1)
	DAILY = datetime.timedelta(days=1)
	WEEKLY = datetime.timedelta(weeks=1)
	MONTHLY = datetime.timedelta(weeks=4)
	CATEGORY_CHOICES = (
		(SECOND, 'Every Second'),
		(MINUTE, 'Every Minute'),
		(HOURLY, 'Hourly'),
		(DAILY, 'Daily'),
		(MONTHLY, 'Monthly'),
		)

	# CONFIRM THESE WORK
	MONDAY = 'Monday'
	TUESDAY = 'Tuesday'
	WEDNESDAY = 'Wednesday'
	THURSDAY = 'Thursday'
	FRIDAY = 'Friday'
	SATURDAY = 'Saturday'
	SUNDAY = 'Sunday'
	DAY_CHOICES = (
		(MONDAY, 'Monday'),
		(TUESDAY, 'Tuesday'),
		(WEDNESDAY, 'Wednesday'),
		(THURSDAY, 'Thursday'),
		(FRIDAY, 'Friday'),
		(SATURDAY, 'Saturday'),
		(SUNDAY, 'Sunday'),
		)

	category = models.CharField(
		max_length=9,
		choices=CATEGORY_CHOICES,
		default=SECOND,
		)
	time = models.TimeField()
	day = models.CharField(
		max_length= 9,
		choices = DAY_CHOICES,
		default = MONDAY,
		)


