from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm

# Create your views here.
def hello(request):
	return render(request, "hello.html", {"name": "alex"})

def index(request):
  return render(request, "index.html")

def signup(request):
	# template = loader.get_template('signup.html')
	return render(request, 'signup.html', {})

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

