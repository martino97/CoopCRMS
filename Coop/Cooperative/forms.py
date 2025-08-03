from django import forms
from django.core.validators import RegexValidator
from .models import CustomerVisitorBook, ATMRegisterBook, StatementRegisterBook, CustomerComplaintBook, InternalTransferBook
import re

class CustomerVisitorBookForm(forms.ModelForm):
    class Meta:
        model = CustomerVisitorBook
        fields = '__all__'

class ATMRegisterBookForm(forms.ModelForm):
    # Define regex validators
    card_number_validator = RegexValidator(
        regex=r'^4198\d{12}$',
        message='Card number must start with 4198 followed by exactly 12 digits (e.g., 4198381008098990)'
    )
    
    account_number_validator = RegexValidator(
        regex=r'^01S\d{10}$',
        message='Account number must start with 01S followed by exactly 10 digits (e.g., 01S2503009781)'
    )
    
    phone_number_validator = RegexValidator(
        regex=r'^\+255\d{9}$',
        message='Phone number must start with +255 followed by exactly 9 digits (e.g., +255769146492)'
    )
    
    # Override fields with validators and custom widgets
    card_number = forms.CharField(
        validators=[card_number_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '4198381008098990',
            'pattern': r'^4198\d{12}$',
            'title': 'Card number must start with 4198 followed by exactly 12 digits'
        }),
        help_text='Format: 4198XXXXXXXXXXXX (16 digits total)'
    )
    
    account_number = forms.CharField(
        validators=[account_number_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '01S2503009781',
            'pattern': r'^01S\d{10}$',
            'title': 'Account number must start with 01S followed by exactly 10 digits'
        }),
        help_text='Format: 01SXXXXXXXXXX (13 characters total)'
    )
    
    customer_phone = forms.CharField(
        validators=[phone_number_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+255769146492',
            'pattern': r'^\+255\d{9}$',
            'title': 'Phone number must start with +255 followed by exactly 9 digits'
        }),
        help_text='Format: +255XXXXXXXXX (13 characters total)',
        required=False
    )
    
    customer_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter customer full name',
            'pattern': r'^[A-Za-z\s]{2,50}$',
            'title': 'Name should contain only letters and spaces (2-50 characters)'
        }),
        help_text='Full name (letters and spaces only)'
    )
    
    request_type = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Card Request, Card Replacement, etc.'
        }),
        help_text='Type of ATM card request'
    )
    
    remarks = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional remarks or notes...'
        }),
        required=False,
        help_text='Optional additional information'
    )

    class Meta:
        model = ATMRegisterBook
        exclude = ['fingerprint', 'request_date', 'status', 'dispatched_by', 'officer_signature']  # Exclude auto-generated fields and officer fields
        
    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if card_number:
            # Remove any spaces or dashes
            card_number = re.sub(r'[\s-]', '', card_number)
            if not re.match(r'^4198\d{12}$', card_number):
                raise forms.ValidationError('Card number must start with 4198 followed by exactly 12 digits')
        return card_number
    
    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        if account_number:
            # Remove any spaces
            account_number = re.sub(r'\s', '', account_number)
            if not re.match(r'^01S\d{10}$', account_number):
                raise forms.ValidationError('Account number must start with 01S followed by exactly 10 digits')
        return account_number
    
    def clean_customer_phone(self):
        phone = self.cleaned_data.get('customer_phone')
        if phone:
            # Remove any spaces, dashes, or parentheses
            phone = re.sub(r'[\s\-\(\)]', '', phone)
            if not re.match(r'^\+255\d{9}$', phone):
                raise forms.ValidationError('Phone number must start with +255 followed by exactly 9 digits')
        return phone
    
    def clean_customer_name(self):
        name = self.cleaned_data.get('customer_name')
        if name:
            # Check if name contains only letters and spaces
            if not re.match(r'^[A-Za-z\s]{2,50}$', name):
                raise forms.ValidationError('Name should contain only letters and spaces (2-50 characters)')
        return name.title() if name else name  # Convert to title case

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
