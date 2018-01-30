from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import (authenticate, login, logout, get_user_model)
from django.views.generic import View
from .forms import UserForm
from .forms import LoginForm
from django import forms

# Create your views here.
def hello(request):
	return render(request, "hello.html", {"name": "alex"})

def index(request):
  return render(request, "index.html")

def signup(request):
	# template = loader.get_template('signup.html')
	return render(request, 'signup.html', {})

# User register form
class UserFormView(View):
	form_class = UserForm
	template_name = 'registration_form.html'

	# GET and POST built in functions

	# Display blank form
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	# Process form data
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():

			user = form.save(commit=False)

			#cleaned (normalized) data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			# Returns user objects if credentials are correct
			user = authenticate(username=username, password=password)

			if user is not None:

				if user.is_active:

					login(request, user)
					return redirect('index')

		return render(request, self.template_name, {'form': form})

# User login form
# def login_view(request):
# 	print(request.user.is_authenticated)
# 	form = LoginForm(request.POST or None)
# 	if form.is_valid():
# 		username = form.cleaned_data.get('username')
# 		password = form.cleaned_data.get('password')
# 		user = authenticate(username=username, password=password)
# 		login(request, user)
# 		print(request.user.is_authenticated)
# 	return render(request, "login_form.html", {'form': form})

def login_view(request):
	print(request.user.is_authenticated)
	form = LoginForm(request.POST or None)
	if request.POST and form.is_valid():
		user = form.login(request)
		if user:
			login(request, user)
			return redirect('index')
	return render(request, 'login_form.html', {'form': form })

















