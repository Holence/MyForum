from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next','/')) # 如果有next就去next，如果没有就去主页
    else:
        form = AuthenticationForm(request)
    
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    
    return redirect("/")

def register_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method=="GET":
        form = UserCreationForm(None)
    elif request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    
    return render(request, "accounts/register.html", {"form": form})
