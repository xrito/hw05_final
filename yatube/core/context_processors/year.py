from django.utils import timezone


def year(request):
    return {
        'y': timezone.now(),
    }
