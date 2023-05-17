from django.shortcuts import render, redirect
from . import models
from . import forms

def create_form2(req):
    if req.method == 'POST':
        form = forms.PostModelForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('/blog/')
    else:    
        form = forms.PostModelForm()

    return render(req, "blog/create_form.html", {'form': form})

def create_form(req):
    if req.method == 'POST':
        form = forms.PostForm(req.POST)
        if form.is_valid():
            new_post = models.Post(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                published_at=form.cleaned_data['published']
            )
            new_post.save()
            return redirect('/blog/')
    else:    
        form = forms.PostForm()

    return render(req, "blog/create_form.html", {'form': form})

def create(req):
    if req.method == 'POST':
        # validation 코드
        new_post = models.Post(
            title=req.POST.get('title'),
            content=req.POST.get('content')
        )
        new_post.save()
        return redirect('/blog/')
    
    return render(req, "blog/create.html")

def detail(req, id):
    post = models.Post.objects.get(id=id)
    return render(req, "blog/detail.html", {
        "post": post
    })
    
def index(req):
    posts = models.Post.objects.all()
    return render(req, "blog/index.html", {
        "post_list": posts
    })
