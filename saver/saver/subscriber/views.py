from django.shortcuts import render
from rest_framework import generics

from . import models, serializers

# Create your views here.
class ClientList(generics.ListAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer

class ClientDetail(generics.RetrieveAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer

class ClientConnections(generics.ListAPIView):
    queryset = models.Connection.objects.all()
    serializer_class = serializers.ConnectionSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(client__pk=self.request.resolver_match.kwargs['client'])

class ClientCommands(generics.ListAPIView):
    queryset = models.Command.objects.all()
    serializer_class = serializers.CommandSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(connection__client__pk=self.request.resolver_match.kwargs['client'])

class ClientResults(generics.ListAPIView):
    queryset = models.Result.objects.all()
    serializer_class = serializers.ResultSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(command__connection__client__pk=self.request.resolver_match.kwargs['client'])
