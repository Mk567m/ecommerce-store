import django_filters
from .models import *

class OrderFilter(django_filters.FilterSet):
  class Meta:
    model = Order
    fields = ['customer','product','date_created','status']
  

