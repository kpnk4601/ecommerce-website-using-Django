from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import View
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import TokenGenerator  # Ensure TokenGenerator is imported correctly
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login,logout

def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        confirm_password = request.POST.get('pass2')

        # Check if passwords match
        if password != confirm_password:
            messages.warning(request, 'Passwords do not match')
            return render(request, 'signup.html')

        # Check if the email is already taken
        if User.objects.filter(username=email).exists():
            messages.info(request, 'Email is already taken')
            return render(request, 'signup.html')

        # Create the user account
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False
        user.save()

        # Prepare activation email
        email_subject = "Activate Your Account"
        message = render_to_string('activate.html', {
            'user': user,
            'domain': request.get_host(),  # Use request.get_host() for better flexibility
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': TokenGenerator().make_token(user)
        })

        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        email_message.send()

        messages.success(request, 'Please check your email to activate your account')
        return redirect('/auth/login')

    return render(request, "signup.html")

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            user = None

        if user is not None and TokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account activated successfully")
            return redirect('/auth/login')

        messages.error(request, "Activation link is invalid")
        return render(request, 'activatefail.html')


def handlelogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Use .get() for safety
        password = request.POST.get('pass1')

        # Authenticate user
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('/')  # Change 'home' to the name of your home URL pattern
        else:
            messages.error(request, "Invalid credentials")
            return redirect('handlelogin')  # Redirect to the login page

    return render(request, "login.html")

def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/auth/login')

