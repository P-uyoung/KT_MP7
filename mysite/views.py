from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages

#로그인
def logout(request):
    request.session.clear()
    #request.session['username'] = username
    return redirect('home')
