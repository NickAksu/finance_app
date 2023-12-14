from rest_framework import serializers
from users.models import User

class UserBaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email"]


class UserMoneySerializer(serializers.Serializer):
    
    fields = {
        "amount": serializers.DecimalField(max_digits=5, decimal_places=2)
    }
    
    def validate(self, attrs):
        attrs["amount"] = round(int(attrs["amount"]), 2)
        return super().validate(attrs)