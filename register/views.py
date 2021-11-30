from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import Registration_Form, UserInfo_Form
from django.contrib.auth.models import User
from social_media import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import generate_token
from .models import Info
# Create your views here.


def home(request):
    return render(request, 'home.html')


def registration(request):
    if request.method == 'GET':
        form = Registration_Form()

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist! Please try some other username.")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(
                request, "Email ID already exist! Please try some other Email ID.")
            return redirect('home')

        if password != cpassword:
            messages.error(request, "Password didn't match!")
            return redirect('home')

        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()

        messages.success(
            request, "Your account is successfully created!! Please check your email to confirm your email address in order to activate your account.")

        current_site = get_current_site(request)
        email_subject = "Confirm your email @Social Media Login!"
        email_message = render_to_string('email_confirmation.html', {
            'name': username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
            'token': generate_token.make_token(new_user)
        })

        email_send = EmailMessage(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [new_user.email]
        )
        email_send.fail_silently = True
        email_send.send()

        return render(request, 'login.html')

    return render(request, 'registration.html', {'form': form})


def loggin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return render(request, 'home.html', {'name': username})
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')
    return render(request, 'login.html')


def loggout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Successfully logged out!')
        return redirect('home')


def user_information(request):
    if request.method == 'POST':
        bdate = request.POST['birthDate']
        mobile = request.POST['mobileNo']
        gender = request.POST['gender']
        city = request.POST['city']
        pin = request.POST['pincode']
        state = request.POST['state']
        id = request.POST['uid']
        image = request.FILES['image']
        file = request.FILES['file']
        print(id)

        user = User.objects.get(pk=id)

        if user is not None:
            new_user = Info(bdate=bdate, mobile=mobile, gender=gender, city=city,
                            pin=pin, state=state, profile_photo=image, document=file, user_id=user)
            new_user.save()
            messages.success(request, "Details are submitted successfully!")
            return redirect('login')

    return render(request, 'error.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        new_user = None

    if new_user is not None and generate_token.check_token(new_user, token):
        new_user.is_active = True
        # user.profile.signup_confirmation = True
        new_user.save()
        # login(request,new_user)
        info_form = UserInfo_Form()
        messages.success(request, "Your Account has been activated!!")
        return render(request, 'user_information.html', {'id': uid, 'info_form': info_form})
    else:
        return render(request, 'error.html')
