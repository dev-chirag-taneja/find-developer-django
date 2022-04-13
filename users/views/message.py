from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import Message, Profile
from users.forms import MessageForm

# Inbox
@login_required()
def inbox(request):
    user         = request.user.profile  
    all_messages = user.receiver.all()                  # getting user all messages
    message      = all_messages.filter(is_read=False)   # filtering with unread messages

    context = {'all_messages':all_messages, 'message':message}
    return render(request, 'users/inbox.html', context)

# View Message
@login_required()
def view_message(request, pk):
    user    = request.user.profile
    message = get_object_or_404(user.receiver, id=pk) # getting user message 
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {'message':message}
    return render(request, 'users/message.html', context)

# Send Message
@login_required()   
def send_message(request, pk):
    form     = MessageForm()
    receiver = get_object_or_404(Profile, id=pk)  # getting receiver username
    sender   = request.user.profile               # getting sender username

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender   = sender
            message.receiver = receiver
            message.save()
            messages.success(request, 'Message sent!')
            return redirect('profile', pk=receiver.id)

    context = {'form':form, 'receiver':receiver}
    return render(request, 'users/contact_form.html', context)