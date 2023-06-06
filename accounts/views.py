from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.forms.models import modelform_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user, update_session_auth_hash
from .models import Account
from .forms import AccountForm

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get("next","home")) # 如果有next就去next，如果没有就去主页
    else:
        form = AuthenticationForm(request)
    
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    
    return redirect("home")

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method=="GET":
        form = UserCreationForm(None)
    elif request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            account = Account.objects.create(user=user)
            account.save()
            return redirect("login")
    
    return render(request, "accounts/register.html", {"form": form})

def accounts_detail_view(request, username):
    if not request.user.is_authenticated:
        return redirect("home")
    
    account = Account.objects.get(user__username=username)

    return render(request, "accounts/detail.html", {"account": account})

def accounts_edit_view(request):
    if not request.user.is_authenticated:
        return redirect("home")
    
    User_Form = modelform_factory(User, fields=["username", "first_name", "last_name", "email"])
    Account_Form = modelform_factory(Account, form=AccountForm, exclude=["user"])
    
    account = Account.objects.get(user=request.user)
    
    # 奶奶的，如果User_Form里instance传入的是request.user
    # 当下面POST如果username invalid时，request.user的username也会被修改掉
    # 去渲染template时，调用request.user就是错误的username
    # 而request.user也没有自带的copy函数，就只能用这个get_user弄一个出来了
    user = get_user(request)
    if request.method=="GET":
        user_form = User_Form(None, instance=user)
        account_form = Account_Form(None, instance=account)
    elif request.method=="POST":
        user_form = User_Form(request.POST, instance=user)
        account_form = Account_Form(request.POST, instance=account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            return redirect("accounts:detail", username=request.user.username)
    
    return render(request, "accounts/edit.html", {"forms": [user_form, account_form]})

def change_password_view(request):
    if not request.user.is_authenticated:
        return redirect("home")
    
    if request.method=="GET":
        form=PasswordChangeForm(request.user)
    elif request.method=="POST":
        form=PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("accounts:detail", username=request.user.username)
    
    return render(request, "accounts/edit.html", {"forms": [form]})