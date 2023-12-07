from .models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages

#로그인
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username is not None:
            existing_user = User.objects.filter(username=username).exists()
            # Redirect to a success page or render a different template
            if existing_user:
                request.session.clear()
                request.session['username'] = username
                return redirect('home')
            else:
                pass
        else:
            #messages.error(request, 'Invalid login credentials')
            #return render(request, 'login/index.html')
            pass
            
    return render(request, 'login/index.html')

# 계정 추가
def add(request):
    username = request.POST.get('sign_username')
    email = request.POST.get('sign_email')
    password = request.POST.get('sign_password')

    if username and email and password:
        existing_user = User.objects.filter(username=username).exists()

        if existing_user:
            message = "already in"
            return JsonResponse({'message': message})
        else:
            new_user = User.objects.create(username=username, email=email, password=password)
            new_user.save()
            message = "added"
            return render(request, 'login/index.html')
    else:
        message = "input all info"
        return JsonResponse({'message': message})
