from django.shortcuts import render
from .forms import SubscribeForm


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.save()
            return render(request, 'subscribers/success.html')
        else:
            form = SubscribeForm()
            return render(request, 'subscribers/subscribe.html', context)
    else:
        form = SubscribeForm()
        context = {
            'form':form,
        }
        return render(request, 'subscribers/subscribe.html', context)
