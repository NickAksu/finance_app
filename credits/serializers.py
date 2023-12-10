from rest_framework import serializers

from credits.models import Credit


class CreditCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Credit
        fields = ["persent", "is_differential"]
        
class CreditSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Credit
        fields = '__all__'
