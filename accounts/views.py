from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:movie_index')
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/forms.html', {
            'form': form
        })

def logout(request):
    auth_logout(request)
    return redirect('movies:movie_index')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            newUser = form.save()
            auth_login(request, newUser)
            return redirect('movies:movie_index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/forms.html', {
        'form': form
    })
    

# def follow(request,user_id):
#     person = get_object_or_404(get_user_model(), pk=user_id)
#     if request.user in person.followers.all():
#         person.followers.remove(request.user)
#     else:
#         person.followers.add(request.user)
#     return redirect('people', person.username)