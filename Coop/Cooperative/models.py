from django.db import models
from django.core.validators import FileExtensionValidator
from PIL import Image
from django.core.files.base import ContentFile
import io

# Create your models here.

class CustomerVisitorBook(models.Model):
    customer_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    visit_date = models.DateTimeField(auto_now_add=True)
    purpose = models.TextField()
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    fingerprint = models.ImageField(upload_to='fingerprints/', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
# In models.py, update the ATMRegisterBook model:
# In Cooperative/models.py, update your ATMRegisterBook model:

class ATMRegisterBook(models.Model):
    """
    Model to store ATM card registration information including customer details and required documents.
    """
    # Customer Information
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    account_number = models.CharField(max_length=100)
    
    # Card Information
    card_number = models.CharField(max_length=100)
    request_type = models.CharField(max_length=100)
    request_date = models.DateTimeField(auto_now_add=True)
    
    # Documents
    signature = models.ImageField(
        upload_to='signatures/', 
        blank=True, 
        null=True
    )
    fingerprint = models.ImageField(
        upload_to='fingerprints/',
        blank=True, 
        null=True,
        verbose_name='Customer Photo'  # This helps identify the field's purpose
    )
    
    # Additional Information
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "ATM Registration"
        verbose_name_plural = "ATM Registrations"
        ordering = ['-request_date']
    
    def __str__(self):
        return f"{self.customer_name} - {self.card_number}"
    
    def save(self, *args, **kwargs):
        if self.fingerprint:
            # Process image before saving
            img = Image.open(self.fingerprint)
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Resize if needed
            if img.size[0] > 800 or img.size[1] > 800:
                img.thumbnail((800, 800))
            # Save processed image
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            self.fingerprint.save(
                self.fingerprint.name,
                ContentFile(buffer.getvalue()),
                save=False
            )
        super().save(*args, **kwargs)

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
