from .models import PageVisit
from django.http import Http404

from django.utils import timezone
from datetime import date

DATE_REFERENCE = date(2024, 3, 29)

def visit_counter_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        if not request.path.startswith('/admin') and not request.path.startswith('/static'):
            today = timezone.now().date()
            day_offset = (today - DATE_REFERENCE).days
            path = request.path
            obj, created = PageVisit.objects.get_or_create(
                path=path, 
                day_offset=day_offset,
                defaults={'visit_count': 0}
            )
            obj.visit_count += 1
            obj.save()
        return response
    return middleware