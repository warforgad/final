from django.shortcuts import render
from rest_framework import generics

from . import models, serializers

# Create your views here.
def index(request):
    return HttpResponse('Lorem ipsum')

class ClientList(generics.ListAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
