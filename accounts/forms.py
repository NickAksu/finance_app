from django import forms

from accounts.models import Account


class PutMoneyForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Account
        fields = ["password", "balance"]
        
class SendMoneyForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    account_id = forms.UUIDField(help_text="Id of account you want to send money to")
    
    class Meta:
        model = Account
        fields = ['password', "balance", "account_id"]
        
        
class ActivateSavingForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ["saving_percent"]
        
class LocalMoneyForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Account
        fields = ["balance"]