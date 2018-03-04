from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie
from .forms import UserCreateForm, UserEditForm, LoginForm, ProfileForm, MedForm, ScheduleForm
from .models import Profile, Medication, Schedule

# Create your views here.
def index(request):
	return render(request, "index.html")

def demo(request):
	return render(request, "demo.html")

@ensure_csrf_cookie
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
@ensure_csrf_cookie
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

@ensure_csrf_cookie
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

@ensure_csrf_cookie
@login_required
def med_info(request):
	if request.method == 'POST':
		med_form = MedForm(request.POST or None)
		if med_form.is_valid():
			pill_name = request.POST.get('pill_name', '')
			module_num = request.POST.get('module_num', '')
			medication_obj = Medication(pill_name=pill_name, module_num=module_num)
			medication_obj.save()
			return redirect('profile/medication')
	else:
		med_form = MedForm()

	return render(request, 'med_info.html', {'form': med_form})

@ensure_csrf_cookie
@login_required
def schedule_view(request):
	schedule_form = ScheduleForm(request.POST or None)

	if request.method == 'POST':
		form = ScheduleForm(request.POST or None)
		if form.is_valid():
			category = request.POST.get('category', '')
			time = request.POST.get('time', '')
			day = request.POST.get('day', '')
			schedule_obj = Schedule(category=category, time=time, day=day)
			schedule_obj.save()
			return redirect('profile/schedule')
	else:
		form = ScheduleForm()


	return render(request, 'med_schedule.html', {'form': schedule_form})














