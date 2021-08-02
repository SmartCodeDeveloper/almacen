from api.models import Notification

def notificationSystem(request):

    notifications = []
    cquantity = 0
    if request.user.is_authenticated:
        cquantity       = Notification.objects.filter(read=False).count()
        notifications   =  Notification.objects.filter(read=False).order_by('-id')[0:5]

    return {
        'cnotifications': notifications,
        'cquantity': cquantity
    }