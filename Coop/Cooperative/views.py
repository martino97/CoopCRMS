from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ATMRegisterBookForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
import base64
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.exceptions import ValidationError
from .utils import process_signature_to_png

@login_required 
def add_customer(request):
    if request.method == 'POST':
        try:
            # Get both photo and signature data
            photo_data = request.POST.get('fingerprint', '')
            signature_data = request.POST.get('signature_data', '')
            
            form = ATMRegisterBookForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                
                # Process photo
                if photo_data and photo_data.startswith('data:image'):
                    try:
                        format, imgstr = photo_data.split(';base64,')
                        img_data = base64.b64decode(imgstr)
                        photo_filename = f'fingerprint_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                        instance.fingerprint.save(photo_filename, ContentFile(img_data), save=False)
                    except Exception as e:
                        print(f"Photo error: {str(e)}")
                        raise ValidationError(f'Error processing photo: {str(e)}')

                # Process signature
                if signature_data and signature_data.startswith('data:image'):
                    try:
                        format, imgstr = signature_data.split(';base64,')
                        img_data = base64.b64decode(imgstr)
                        sig_filename = f'signature_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                        instance.signature.save(sig_filename, ContentFile(img_data), save=False)
                    except Exception as e:
                        print(f"Signature error: {str(e)}")
                        raise ValidationError(f'Error processing signature: {str(e)}')

                # Save the instance
                instance.save()
                messages.success(request, 'Customer added successfully!')
                return redirect('dashboard')
            else:
                print(f"Form errors: {form.errors}")
                messages.error(request, f'Form validation failed: {form.errors}')
        except Exception as e:
            print(f"Error saving customer: {str(e)}")
            messages.error(request, str(e))
    else:
        form = ATMRegisterBookForm()
    
    return render(request, 'add_customer.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomerVisitorBookForm

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'sign-up.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard view (ensure @login_required)
@login_required
def dashboard(request):
    try:
        from .models import ATMRegisterBook
        atm_cards = ATMRegisterBook.objects.all()
        # Add debug logging
        for card in atm_cards:
            print(f"Card {card.id} fingerprint: {card.fingerprint}")
    except Exception as e:
        print(f"Error fetching ATM cards: {e}")
        atm_cards = []
    
    return render(request, 'home-2.html', {'atm_cards': atm_cards})

# Signature recapture view
import base64
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

@csrf_exempt
def recapture_signature(request):
    if request.method == 'POST':
        data_url = request.POST.get('signature_data')
        if data_url and data_url.startswith('data:image/png;base64,'):
            format, imgstr = data_url.split(';base64,')
            img_data = base64.b64decode(imgstr)
            from .models import ATMRegisterBook
            latest_card = ATMRegisterBook.objects.order_by('-id').first()
            if latest_card:
                # Save to fingerprint field
                latest_card.fingerprint.save('fingerprint.png', ContentFile(img_data), save=True)
        return HttpResponseRedirect('/dashboard/')
    return HttpResponseRedirect('/dashboard/')

# Example: Customer Visitor Book form view
@login_required
def add_visitor(request):
    if request.method == 'POST':
        form = CustomerVisitorBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CustomerVisitorBookForm()
    return render(request, 'add-product.html', {'form': form})
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from twilio.rest import Client

TWILIO_ACCOUNT_SID = 'ACc3bd0c47c5a8b221360e37f69d897cd1'
TWILIO_AUTH_TOKEN = '85cfc84af53daf203827e9ad2efabcd0'
TWILIO_PHONE_NUMBER = '+18146793789'  # <-- Replace with your Twilio phone number in E.164 format, e.g. '+14155552671'

@csrf_exempt
def send_mass_sms(request):
    if request.method == "POST":
        data = json.loads(request.body)
        messages = data.get('messages', [])
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        for msg in messages:
            # Only verified numbers will receive SMS on free trial
            try:
                client.messages.create(
                    body=msg['message'],
                    from_=TWILIO_PHONE_NUMBER,
                    to=msg['phone']  # This must also be in E.164 format, e.g. '+2557XXXXXXX'
                )
            except Exception as e:
                print(f"Failed to send to {msg['phone']}: {e}")
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def mobile_signature(request):
    """Handle mobile signature photo capture"""
    if request.method == 'POST' and request.FILES.get('signature'):
        try:
            signature_file = request.FILES['signature']
            # Process file and return processed signature
            # Add your processing logic here
            return JsonResponse({'status': 'success', 'data': processed_signature})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request, 'mobile_signature.html')
