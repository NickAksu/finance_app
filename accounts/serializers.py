from rest_framework import serializers

from accounts.models import Account, Operation

class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ["account_id", "saving_percent", "balance", "is_activated", "saving_percent"]
