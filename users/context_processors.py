# Show number of messages in navbar inbox icon
def inbox(request):

    if request.user.is_authenticated:
        user         = request.user.profile
        all_messages = user.receiver.all()
        message      = all_messages.filter(is_read=False)
    else:
        message = []

    return {'message':message}