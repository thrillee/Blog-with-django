from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from blogApp.models import Post

@login_required
def user_profile(request, username=None):
    user = get_object_or_404(User, username=username)
    if str(request.user) == str(username):
        post = Post.objects.all().filter(status='draft', author=request.user,)
        for i in post:
            print(i)
    else:
        post = None
    context = {
        'user':user,
        'drafts':post,
    }
    return render(request, 'profiles/profile.html',context)
