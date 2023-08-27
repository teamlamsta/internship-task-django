from rest_framework import serializers

from home.models import UrlShortner

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlShortner
        fields = ['incoming_url', 'outgoing_url']

class UrlAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlShortner
        fields = ['incoming_url', 'outgoing_url', "is_active", "click_through_counter"]

