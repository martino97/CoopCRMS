from django.db import models

# Create your models here.

class CustomerVisitorBook(models.Model):
    customer_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    visit_date = models.DateTimeField(auto_now_add=True)
    purpose = models.TextField()
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    fingerprint = models.ImageField(upload_to='fingerprints/', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

class ATMRegisterBook(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    account_number = models.CharField(max_length=100)
    card_number = models.CharField(max_length=100)
    request_type = models.CharField(max_length=100)  # e.g., New, Replacement
    request_date = models.DateTimeField(auto_now_add=True)
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    fingerprint = models.ImageField(upload_to='fingerprints/', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

class StatementRegisterBook(models.Model):
    customer_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=100)
    statement_period = models.CharField(max_length=100)
    request_date = models.DateTimeField(auto_now_add=True)
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    fingerprint = models.ImageField(upload_to='fingerprints/', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

class CustomerComplaintBook(models.Model):
    customer_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    complaint_date = models.DateTimeField(auto_now_add=True)
    complaint_details = models.TextField()
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    fingerprint = models.ImageField(upload_to='fingerprints/', blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)

class InternalTransferBook(models.Model):
    customer_name = models.CharField(max_length=255)
    from_account = models.CharField(max_length=100)
    to_account = models.CharField(max_length=100)
    transfer_amount = models.DecimalField(max_digits=12, decimal_places=2)
    transfer_date = models.DateTimeField(auto_now_add=True)
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    fingerprint = models.ImageField(upload_to='fingerprints/', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
