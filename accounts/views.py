from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    context={}
    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm(request)

    context={
        "form": form
    }
    
    return render(request, "accounts/login.html", context)

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    
    return redirect("/")

def register_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("/")
    
    context={
        "form": form
    }
    return render(request, "accounts/register.html", context)
