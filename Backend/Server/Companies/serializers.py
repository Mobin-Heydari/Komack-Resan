from rest_framework import serializers

from .models import *

from Server.settings import ALLOWED_HOSTS




class FirstItemSerializers(serializers.ModelSerializer):

    icon = serializers.SerializerMethodField()

    class Meta:
        model = FirstItem
        fields = "__all__"

    def get_icon(self, obj):

        icon = str(obj.icon)
        
        if ALLOWED_HOSTS == []:
            path_host = "http://127.0.0.1:8000"
        else:
            path_host = ALLOWED_HOSTS[0]
        icon = f"{path_host}/media/{icon}"


class SecondItemSerializers(serializers.ModelSerializer):

    icon = serializers.SerializerMethodField()

    class Meta:
        model = SecondItem
        fields = "__all__"
    
    def get_icon(self, obj):
        
        icon = str(obj.icon)
        
        if ALLOWED_HOSTS == []:
            path_host = "http://127.0.0.1:8000"
        else:
            path_host = ALLOWED_HOSTS[0]
        icon = f"{path_host}/media/{icon}"
