from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from .forms import RegisterForm
from .decorators import unauthenticated_user
from django.contrib.auth.views import LoginView


@unauthenticated_user
def register_view(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'registration/register.html', locals())
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, "Bonjour " + username + " !")
            return redirect('home')

    return render(request, 'registration/register.html', locals())


def logout_view(request):
    logout(request)
    messages.info(request, "Vous êtes bien déconnecté")
    return redirect('home')


@login_required
def profile_view(request):
    return render(request, 'account/profile.html')



@login_required
def favorite_view(request, product_id, sub_id):
    pass
