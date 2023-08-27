from rest_framework import serializers

from home.models import UrlShortner

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlShortner
        fields = ['incoming_url', 'outgoing_url', 'click_through_counter', 'is_active']
