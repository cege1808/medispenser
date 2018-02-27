from django.contrib.auth.models import User
from django.contrib.auth import (authenticate, login, logout, get_user_model)
from django import forms
from .models import Profile
# from .models import Medication

# User Registration Form
class UserCreateForm(forms.ModelForm):
	email2 = forms.EmailField(label='Confirm Email')
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['first_name','last_name','username', 'email', 'email2','password']

	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Emails must match")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")
		return email

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email']

# User login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        print("user: {}".format(user))
        if not user:
        	raise forms.ValidationError("Login invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number',)

class MedForm(forms.Form):
    # class Meta:
    #     model = Medication
    #     fields = ['pill_name', 'module_num']
    pill_name = forms.CharField(max_length=255)
    module_num = forms.CharField(max_length=255)



