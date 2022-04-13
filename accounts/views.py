from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .forms import CustomUserCreationForm
from .tokens import generate_token

# Create your views here.

# Send email
def send_email(user, request):

    current_site  = get_current_site(request)
    email_subject = 'Activate your account!'
    email_body    = render_to_string('accounts/activate_account.html',{
        'user':user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    email = EmailMessage(subject=email_subject, body=email_body, from_email=from_email, to=recipient_list)
    return email.send(fail_silently=False)
        
# Register
def register_user(request):

    # checking if user is authenticated
    if request.user.is_authenticated:
        return redirect('home')

    form = CustomUserCreationForm()
    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_email(user, request)
            messages.success(request, 'Account verification link has been sent to your email address!')
            return redirect('login') 

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

# Login
def login_user(request):

    # checking if user is authenticated
    if request.user.is_authenticated:
        return redirect('home')

    # getting credentials
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist, please signup!')
            return redirect('register')
        
        # authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            messages.success(request, f'Welcome {user.username}!')
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'home')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'accounts/login.html')

# Logout
@login_required()
def logout_user(request):
    logout(request)
    return redirect('home')

# Activate Account
def activateUser(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # checking if user exist and token is valid
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Your account has been verified!')
        return redirect('account')
    else:
        messages.warning(request, 'Activation link is invalid or expired, enter your email address!')      
        return redirect('generate_link')

# Generate Link
def generateLink(request):

    if request.method == 'POST':   

        # getting email   
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
            
        # sending email to user 
        if user is not None:
            send_email(user, request)   
            messages.success(request, f"Verification link has been sent to your email.")
            return redirect('login')
        else:
            messages.warning(request, f"Account does not exist, please signup!")
            return redirect('register')
    return render(request, 'accounts/generate_link.html')

# Change password
@login_required()
def change_password(request):

    if request.method == 'POST':
        old_password     = request.POST['old_password']
        new_password     = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        # checking user old password
        user = User.objects.get(username=request.user.profile)
        check_password = user.check_password(old_password)
        
        # checking and changing user new password 
        if check_password:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                logout(request)
                messages.success(request, 'Your password has been changed!')
                return redirect('login')
            else:
                messages.error(request, 'Password does not matched!')
        else:
            messages.error(request, 'Old password is incorrect!')
            
    return render(request,'accounts/change_password.html')