from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from urllib.parse  import quote_plus
from .forms import CommentForm , Update_Post#, LikeBtn
from .models import *
from django.urls import reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from profiles.models import UserProfile

@login_required
def create_post(request):

    if request.user.is_staff == True or request.user.is_superuser == True:
        if request.method == 'POST':
            form = Update_Post(request.POST)
            if form.is_valid():
                update = form.save(commit=False)
                update.save()
                print(request.user.is_staff == True or request.user.is_superuser == True)
                if update.status == 'draft':
                    return HttpResponseRedirect(reverse('profiles:user_profile', args=[update.author]))
                return HttpResponseRedirect(reverse('blogApp:post_details', args=[update.slug]))
        else:
            form = Update_Post()
            context = {
                'form':form,
            }
        return render(request, 'blogApp/update.html', context)
    else:
        raise Http404

@login_required
def post_update(request, post=None):
    instance = get_object_or_404(Post, slug=post)
    if request.user == instance.author and request.user.is_staff == True or request.user.is_superuser == True:
        if request.method == 'POST':
            form = Update_Post(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                update = form.save(commit=False)
                update.save()
                if update.status == 'draft':
                    return HttpResponseRedirect(reverse('profiles:user_profile', args=[update.author]))
                return HttpResponseRedirect(reverse('blogApp:post_details', args=[update.slug]))
        else:
            form = Update_Post(instance=instance)
            context = {
                    'form':form,
                    }
            return render(request, 'blogApp/update.html', context)
    else:
        raise Http404

@login_required
def delete_post(request, post=None):
    instance = get_object_or_404(Post, slug=post,)
    if instance.author == request.user and request.user.is_staff == True or request.user.is_superuser == True:
        if request.method == 'POST':
            instance.delete()
            return HttpResponseRedirect(reverse('blogApp:post_list', args=['9ja']))
        else:
            context = {
                'title':instance.title,

                'slug':instance.slug,
                }
            return render(request, 'blogApp/delete.html', context)
    else:
        raise Http404


def post_details(request, post=None,):
    instance = get_object_or_404(Post, slug=post, status='published')
    users = get_object_or_404(User, post=instance)
    share_string = quote_plus(instance.content)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.posts = instance
            comment.save()
            return HttpResponseRedirect(reverse('blogApp:post_details', args=[post]))
        else:
            form = CommentForm()
            return HttpResponseRedirect(reverse('blogApp:post_details', args=[post]))
    else:
        form = CommentForm()
        context = {
            'user': users,
            'author':instance.author,
            'time': instance.created_at,
            'title':instance.title,
            'content':instance.content,
            'comments':instance.comment_post,
            'no_of_comments':len(instance.comment_post),
            'slug':instance.slug,
            'form':form,
            'share_string':share_string,
            'image':instance.image,

        }
        return render(request, 'blogApp/details.html',context)

def post_list(request, category=None):
    posts = Post.objects.all().filter(status='published',category=category)
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(author__first_name__icontains=query)
            ).distinct()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    context = {
        'posts':contacts,
        'title':'Posts',
        }
    return render(request,'blogApp/post_lists.html',context)

# def like_post(request, post=None):
#     instance = get_object_or_404(Post, slug=post, status='published')
#     form = CommentForm()
#     if instance.like == False:
#         instance.like = True
#         instance.like_no += 1
#     else:
#         instance.like = False
#         instance.like_no -= 1
#     instance.save()
#
#     context = {
#         'slug':instance.slug,
#         'title':instance.title,
#         'content':instance.content,
#         'comments':instance.comment_post,
#         'likes':instance.like_no,
#         'form':form,
#         }
#     return HttpResponseRedirect(reverse('blogApp:post_details', args=[post]))

def post_comment(request, post=None):
    instance = get_object_or_404(Comment, slug=post, status='published')
    comments = len(instance.post)
    context = {
        'posts':posts,
        'title':'Posts',
        'comments':comments,
        }
    return render(request,'blogApp/post_lists.html',context)

def listing(request):
    contact_list = Contacts.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'list.html', {'contacts': contacts})

def send_text(request):
    return 'django_twilio.views.message', {
        'message': 'Yo!',
        'to': '08064382633',
        'sender': '08154396918',
        'status_callback': '/message/completed/',
    }
