from rest_framework import serializers

class TestSerializer(serializers.Serializer):
    message = serializers.CharField()
    user_id = serializers.CharField()
    supabase_response = serializers.DictField(allow_null=True)