from django import forms
from .models import CustomerVisitorBook, ATMRegisterBook, StatementRegisterBook, CustomerComplaintBook, InternalTransferBook

class CustomerVisitorBookForm(forms.ModelForm):
    class Meta:
        model = CustomerVisitorBook
        fields = '__all__'

class ATMRegisterBookForm(forms.ModelForm):
    class Meta:
        model = ATMRegisterBook
        exclude = ['fingerprint']

class StatementRegisterBookForm(forms.ModelForm):
    class Meta:
        model = StatementRegisterBook
        fields = '__all__'

class CustomerComplaintBookForm(forms.ModelForm):
    class Meta:
        model = CustomerComplaintBook
        fields = '__all__'

class InternalTransferBookForm(forms.ModelForm):
    class Meta:
        model = InternalTransferBook
        fields = '__all__'
