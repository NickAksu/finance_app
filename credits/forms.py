from django import forms

from credits.models import Credit


class CreditForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_differential = forms.BooleanField(required=False)
    period = forms.IntegerField(required=True)
    
    class Meta:
        model = Credit
        fields = ["password", "persent", "total_sum", "is_differential", "period"]
