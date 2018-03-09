from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.template.response import TemplateResponse

from .forms import UserCreateForm, UserEditForm, LoginForm, ProfileForm, MedForm, ScheduleForm
from .models import Profile, Medication, Schedule

# Create your views here.
def index(request):
	return render(request, "index.html")

def demo(request):
	return render(request, "demo.html")

@transaction.atomic
def create_user(request):

		user_form = UserCreateForm(request.POST or None)
		profile_form = ProfileForm(request.POST or None)

		if request.method == 'POST':
			user_form = UserCreateForm(request.POST)
			profile_form = ProfileForm(request.POST)

			if user_form.is_valid() and profile_form.is_valid():
				user = user_form.save(commit=False)
				username = user_form.cleaned_data['username']
				password = user_form.cleaned_data['password']
				user.set_password(password)
				user.save()

				profile_form = ProfileForm(request.POST, instance=user.profile)
				profile_form.save()

				# Returns user objects if credentials are correct
				user = authenticate(username=username, password=password)

				if user is not None:
					if user.is_active:
						login(request, user)
						return redirect('index')
			else:
				messages.error(request, 'Please correct the error below.')

		return render(request, 'registration.html', {'form': [*user_form, *profile_form]})

# User login form
def login_view(request):
	form = LoginForm(request.POST or None)

	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')

		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('index')

	else:
		return render(request, "login.html", {'form': form})

# User logout
@login_required
def logout_view(request):
	logout(request)
	return redirect('index')


@login_required
@transaction.atomic
def edit_profile(request):

		user_form = UserEditForm(request.POST or None, instance=request.user)
		profile_form = ProfileForm(request.POST or None, instance=request.user)

		try:
			user_profile = Profile.objects.get(user=request.user)
		except Profile.DoesNotExist:
			messages.error(request, 'Invalid user_profile!')
			return render(request, 'profile.html', {'form': [*user_form, *profile_form]})


		if request.method == 'POST':
			user_form = UserEditForm(request.POST, instance=request.user)
			profile_form = ProfileForm(request.POST, instance=request.user.profile)
			if user_form.is_valid() and profile_form.is_valid():
				user_form.save()
				profile_form.save()
				messages.success(request, 'Your profile was successfully updated!')
				return redirect('profile/edit')
			else:
				messages.error(request, 'Please correct the error below.')
		else:
			user_form = UserEditForm(instance=request.user)
			profile_form = ProfileForm(instance=request.user.profile)
		return render(request, 'profile.html', {'form': [*user_form, *profile_form]})


@login_required
def medication(request):
	medication_data = list(request.user.medication_set.all().order_by('module_num'))
	schedule_data = list(request.user.schedule_set.all())

	for schedule in schedule_data:
		schedule.module_nums = [int(x) for x in schedule.module_nums.split(',') ]

	return render(request, 'medication.html', {'medication_data': medication_data, 'schedule_data': schedule_data})

@login_required
def new_medication(request):
	med_form= MedForm(request.POST or None, request.FILES or None)
	if med_form.is_valid():
		fs=med_form.save(commit=False)
		fs.user=request.user
		fs.save()
		return redirect('profile/medication')
	return render(request, 'new_medication.html', {'form': med_form})

@login_required
def edit_medication(request):
	try:
		med_id = request.GET['med'][0]
		med_info = Medication.objects.get(id=med_id)
	except Medication.DoesNotExist:
		messages.error(request, 'Invalid medication!')
		return medication(request)

	med_form= MedForm(request.POST or None, instance=med_info)

	if request.method == 'POST':
		if med_form.is_valid():
			fs=med_form.save(commit=False)
			fs.user=request.user
			fs.save()
			return redirect('profile/medication')
	return render(request, 'edit_medication.html', {'form': med_form})

@login_required
def delete_medication(request):
	try:
		med_id = request.GET['med'][0]
		med_info = Medication.objects.get(id=med_id)
	except Medication.DoesNotExist:
		messages.error(request, 'Invalid medication!')
		return medication(request)

	try:
		delete_reply = request.GET['delete_reply']
		if delete_reply == 'yes':
			med_info.delete()
			print('delete meds')
		return medication(request)
	except Exception:
		pass

	return render(request, 'delete_medication.html', {'med': med_info})

@login_required
def schedule_view(request):
	schedule_form = ScheduleForm(request.POST or None, request.FILES or None)

	if schedule_form.is_valid():
		fs=schedule_form.save(commit=False)
		fs.user=request.user
		fs.save()
		return redirect('profile/schedule')

	return render(request, 'med_schedule.html', {'form': schedule_form})




