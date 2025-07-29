# Add customer view
from .forms import ATMRegisterBookForm

def add_customer(request):
    import base64
    from django.core.files.base import ContentFile
    if request.method == 'POST':
        form = ATMRegisterBookForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            canvas_data = request.POST.get('fingerprint_canvas')
            if canvas_data and canvas_data.startswith('data:image/png;base64,'):
                format, imgstr = canvas_data.split(';base64,')
                img_data = base64.b64decode(imgstr)
                instance.fingerprint.save('fingerprint_canvas.png', ContentFile(img_data), save=False)
            camera_data = request.POST.get('fingerprint_camera')
            if (not canvas_data or not canvas_data.startswith('data:image/png;base64,')) and camera_data and camera_data.startswith('data:image/png;base64,'):
                format, imgstr = camera_data.split(';base64,')
                img_data = base64.b64decode(imgstr)
                instance.fingerprint.save('fingerprint_camera.png', ContentFile(img_data), save=False)
            instance.save()
            return redirect('dashboard')
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
    from .models import ATMRegisterBook
    atm_cards = ATMRegisterBook.objects.all()
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
