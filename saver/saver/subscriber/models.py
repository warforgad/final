import shortuuid
from django.db import models

class Client(models.Model):
    client_name = models.CharField(max_length=64)
    client_version = models.CharField(max_length=10)
    created_time = models.DateTimeField()
    
class Connection(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_uuid = models.CharField(max_length=shortuuid.ShortUUID()._length)
    connection_time = models.DateTimeField()
    
class Command(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    transaction_uuid = models.CharField(max_length=shortuuid.ShortUUID()._length)
    command = models.CharField(max_length=100)
    sent_time = models.DateTimeField()

class Result(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    result = models.CharField(max_length=1024)
    received_time = models.DateTimeField()
