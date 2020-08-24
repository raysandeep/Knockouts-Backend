import csv

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.models import User


class Health(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(status=204)


def download_csv(request, queryset):
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response


def myview(request):
    data = download_csv(request, User.objects.all())

    return HttpResponse(data, content_type='text/csv')
