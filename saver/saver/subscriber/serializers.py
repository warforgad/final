from rest_framework import serializers
from . import models

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = ('id', 'client_name', 'client_version', 'created_time')

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Connection
        fields = ('id', 'client_uuid', 'connection_time')

class CommandSerializer(serializers.ModelSerializer):
    client_uuid = serializers.SerializerMethodField()

    class Meta:
        model = models.Command
        fields = ('id', 'client_uuid', 'transaction_uuid', 'command', 'sent_time')

    def get_client_uuid(self, obj):
        return obj.connection.client_uuid

class ResultSerializer(serializers.ModelSerializer):
    client_uuid = serializers.SerializerMethodField()
    command = serializers.SerializerMethodField()
    transaction_uuid = serializers.SerializerMethodField()

    class Meta:
        model = models.Result
        fields = ('id', 'client_uuid', 'command', 'transaction_uuid', 'result', 'received_time')

    def get_client_uuid(self, obj):
        return obj.command.connection.client_uuid

    def get_command(self, obj):
        return obj.command.command

    def get_transaction_uuid(self, obj):
        return obj.command.transaction_uuid
