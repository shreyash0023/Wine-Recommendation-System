from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

# Create your views here.
def signup_view(request):
	#submit_data = request.POST
	if request.method == 'POST':
		#validate the data we got from the submit button
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			# username = request.POST['username']
			# password = request.POST['password1']
			# user = authenticate(username=username,password=password)
			# log the user ins
			#login(request, user)
			return redirect('search:display_wines')
		else:
			err = form.error_messages.keys()
			mes = []

			keys = []

			for key in form.errors:
				keys.append(key)

			messages = []
			for x in keys:
				for y in form.errors[x]:
					messages.append(y)
	
			if len(messages) >=2 and messages[0] == messages[1]:
				messages.pop()

			if len(messages) >=2 and messages[0] == messages[1]:
				messages.pop()

			return render(request,'accounts/signup.html',{'form':form,'er':form.errors,'dis':messages})

	else:
		form = UserCreationForm()

	return render(request,'accounts/signup.html',{'form':form})


def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			#Login the user
			user = form.get_user()
			login(request,user)
			return redirect('search:display_wines')

		else:

			err = form.error_messages.keys()
			mes = []

			keys = []

			for key in form.errors:
				keys.append(key)

			messages = []
			for x in keys:
				for y in form.errors[x]:
					messages.append(y)
		
			if len(messages) >=2 and messages[0] == messages[1]:
				messages.pop()

			return render(request,'accounts/login.html',{'form':form,'er':form.errors,'dis':messages,'username':request.POST['username'],'pass':request.POST['password']})

	else:
		form = AuthenticationForm()


	return render(request,'accounts/login.html',{'form':form})






















