from django.contrib import messages
from django.shortcuts import redirect, render
from task_manager.forms import SignupForm
from task_manager.models import Task


def home(request):
    tasks = Task.objects.all()

    return render(request, 'home.html', context={
        'tasks': tasks,
    })


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                'Account was created for {0}'.format(username),
            )
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', context={
        'form': form,
    })
