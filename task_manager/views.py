from django.shortcuts import render, redirect
from task_manager.forms import SignupForm


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', context={
            'form': form,
    })
