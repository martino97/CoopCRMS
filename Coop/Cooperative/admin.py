from django.contrib import admin

from .models import ATMRegisterBook

@admin.register(ATMRegisterBook)
class ATMRegisterBookAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name', 'customer_phone', 'account_number', 'card_number',
        'request_type', 'request_date', 'signature', 'fingerprint', 'remarks'
    )
