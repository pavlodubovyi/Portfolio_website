from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    return render(request, "pages/home.html", {})


def about(request):
    return render(request, "pages/about.html", {})


def contact(request):
    return render(request, "pages/contact.html", {})


def hire(request):
    if request.method == "POST":
        name = request.POST.get("name")
        company = request.POST.get("company", "Unknown")
        email = request.POST.get("email")
        message = request.POST.get("message")

        full_message = f"Name: {name}\nCompany: {company}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(
            subject="Potential Job Offer",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )

        return redirect("home")

    return render(request, "pages/hire.html", {})
