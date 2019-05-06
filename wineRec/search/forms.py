from django import forms
from django.contrib.auth import authenticate 
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()


# All the labels in the form must correspond to the models defined earlier 

# class WineForm(forms.ModelForm):
# 	class Meta:
# 		model = Wine 
# 		fields = ('country','price','points')
# 	pass


# class UserLogin(forms.Form):
# 	username = forms.CharField()
# 	password = forms.CharField(widget=forms.PasswordInput)

# 	def clean(self,*args,**kwargs):
# 		username = self.cleaned_data.get('username')
# 		password = self.cleaned_data.get('password')

# 		if username and password:
# 			user = authenticate(username=username,password=password)
# 			if not user:
# 				raise forms.ValidationError('This user does not exit')
# 			if not password:
# 				raise forms.ValidationError('Incorrect password')
# 			if not user.is_active:
# 				raise forms.ValidationError('This user is not active')

# 		return super(UserLoginForm, self).clean(*args,**kwargs)



# class UserRegisterForm(forms.ModelForm):
# 	email = forms.EmailField(label='Email Address')
# 	email2 = forms.EmailField(label='Confirm Email')
# 	password = forms.CharField(widget=forms.PasswordInput)

# 	class Meta:
# 		model = User
# 		fields = [
# 		'username',
# 		'email',
# 		'email2',
# 		'password' ]

# 	def clean(self):
# 		email = self.cleaned_data.get('email')
# 		email2 = self.cleaned_data.get('email2')

# 		if email2 != email:
# 			raise forms.ValidationError('Emails must match')

# 		email_qs = User.Objects.filter(email=email)
# 		if email_qs.exists():
# 			raise froms.ValidationError(
# 				'This email already exists'
# 				)

# 		return email























