from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape



class OrderListNotificationJson(BaseDatatableView):
    order_columns = ['-id']

    def get_initial_queryset(self):
        return  Notification.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            print(search)
            qs = qs.filter(Q(message__istartswith=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                escape("{0}".format(item.id)),
                "{0}/{1}/{2}".format(item.date_created.day, item.date_created.month, item.date_created.year),
                "{0}".format(item.message)
            ])
            
        return json_data