from django.forms import widgets
from rest_framework import serializers
from .models import URLExp

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLExp
        fields = ('id', 'shorturl', 'httpstat', 'finaldestination', 'pagetitle', 'imagecap')