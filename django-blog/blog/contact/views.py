from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContatForm
from django.conf import settings

def contact(request):
    title = 'Contact'
    form = ContatForm(request.POST or None)
    confirm = None
    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        subject = 'Message from MYSITE.com'
        message = '{} by  {}'.format(comment,name)
        emailFrom = form.cleaned_data['email']
        emailTo = [settings.EMAIL_HOST_USER]
        send_mail(subject,message,emailFrom,emailTo,fail_sliently=True)
        title = 'Thanks'
        confirm = 'Thanks for the message we will get right back back to you.'
        form = None
    context = {'title':title, 'confirm':confirm, 'form':form}
    template = 'contact.html'
    return render(request,template,context)
