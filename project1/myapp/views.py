from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from datetime import datetime

from django.contrib.auth.models import User
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.
date = datetime.now()


@login_required(login_url="log_in")
def home(request):
    return render(request, "myapphtml/home.html", {"date": date})


def about(request):
    return render(request, "myapphtml/about.html", {"date": date})


@login_required(login_url="log_in")
def service(request):
    return render(request, "myapphtml/service.html", {"date": date})


@login_required(login_url="log_in")
def menu(request):
    return render(request, "myapphtml/menu.html", {"date": date})


def advice(request):
    return render(request, "myapphtml/advice.html", {"date": date})


def contact(request):
    if request.method == "POST":
        firstname = request.POST.get("fname")
        lastname = request.POST.get("lname")
        email = request.POST.get("email")
        dropdown = request.POST.get("choose")
        phone = request.POST.get("phone")
        texts = request.POST.get("texts")

        detail = CDetails.objects.create(
            firstname=firstname,
            lastname=lastname,
            email=email,
            dropdown=dropdown,
            phone=phone,
            texts=texts,
        )
        detail.save()
        messages.success(request, "Your Form has been successfully submitted")

        send_mail(
            subject="Momos",
            message=texts,
            from_email="anishnepal000@gmail.com",
            recipient_list=[email],
        )
        return redirect("home")
    return render(request, "myapphtml/contact.html")


def terms(request):
    return render(request, "footers/terms.html", {"date": date})


def policy(request):
    return render(request, "footers/policy.html", {"date": date})


def support(request):
    return render(request, "footers/support.html", {"date": date})


# =====================================================
# ========================================================
# Auth section starts
def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        check = request.POST.get("check")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username is not register")
            return redirect("log_in")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if check:
                request.session.set_expiry(86400)
            else:
                request.session.set_expiry(0)

            messages.success(request, "Successfully Login!!!")
            return redirect("home")

    return render(request, "auth/login.html")


def register(request):
    if request.method == "POST":
        firstname = request.POST.get("fname")
        lastname = request.POST.get("lname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        try:
            if not re.search(r"[A-Z]", password):
                messages.error(
                    request, "Password must contain atleast one capital letter"
                )
                return redirect("register")
            if not re.search(r"\d", password):
                messages.error(request, "Password must contain atleast one digit")
                return redirect("register")
            if not re.search(r"[!@#$%^&*()]", password):
                messages.error(
                    request, "Password must contain atleast one special character"
                )
                return redirect("register")
            validate_password(password)
            if password == cpassword:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                    return redirect("register")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect("register")
                else:
                    User.objects.create_user(
                        first_name=firstname,
                        last_name=lastname,
                        username=username,
                        email=email,
                        password=password,
                    )
                    messages.success(request, "User has been successfully register ")
                    return redirect("log_in")
            else:
                messages.error(request, "Password must be same.")
                return redirect("register")
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect("register")

    return render(request, "auth/register.html")


def log_out(request):
    logout(request)
    return redirect("log_in")


def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("log_in")
    return render(request, "auth/change_password.html", {"form": form})


# Auth section ends
