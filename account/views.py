from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

# Create your views here.

def signup(request):
	if request.method == "POST":
		if request.POST['pw1'] == request.POST['pw2']:
			try:
				User.objects.get(username=request.POST['username'])
				error = 'Username has already been used'
				msg = dict()
				msg['error'] = error
				return render(request, 'accounts/signup.html', msg)
			except User.DoesNotExist:
				user = User.objects.create_user(request.POST['username'], \
					password=request.POST['pw1'])
				login(request, user)
				return redirect('home')
		else:
			error = 'Passwords do not match'
			msg = dict()
			msg['error'] = error
			return render(request, 'accounts/signup.html', msg)
	else:
		return render(request, 'accounts/signup.html')

def loginview(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			if 'next' in request.POST:
				return redirect(request.POST['next'])
			#redirect to a successful page
			success = 'Logged in Successfully!'
			msg = dict()
			msg['info'] = success
			return redirect('home')
		else:
			error = 'Username or password does not match'
			msg = dict()
			msg['info'] = error
			return render(request, 'accounts/login.html', msg)
	else:
		return render(request, 'accounts/login.html')

def logoutview(request):
	if request.method == "POST":
		logout(request)
		return redirect('home')
