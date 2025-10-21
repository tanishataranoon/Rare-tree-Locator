# DonationApp/views.py
import uuid, requests
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from .models import Donation
from .forms import DonationForm
from django.http import HttpResponseRedirect
import json
from django.http import JsonResponse




# ------------------- Initiate Donation -------------------
@login_required
def initiate_donation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            order_id = f"TREE-{uuid.uuid4().hex[:8].upper()}"

            donation = Donation.objects.create(
                user=request.user,
                amount=amount,
                order_id=order_id
            )

            payload = {
                'store_id': settings.SSLC_STORE_ID,
                'store_passwd': settings.SSLC_STORE_PASS,
                'total_amount': amount,
                'currency': 'BDT',
                'tran_id': order_id,
                'success_url': request.build_absolute_uri('/donate/success/'),
                'fail_url': request.build_absolute_uri('/donate/fail/'),
                'cancel_url': request.build_absolute_uri('/donate/cancel/'),
                'ipn_url': request.build_absolute_uri('/donate/ipn/'),

                'cus_name': request.user.get_full_name() or request.user.username,
                'cus_email': request.user.email or 'demo@email.com',
                'cus_add1': 'N/A',
                'cus_city': 'Dhaka',
                'cus_postcode': '1000',
                'cus_country': 'Bangladesh',
                'cus_phone': '017XXXXXXXX',
                'shipping_method': 'NO',
                'product_name': 'Tree Donation',
                'product_category': 'Donation',
                'product_profile': 'general'
            }

            try:
                response = requests.post(
                    'https://sandbox.sslcommerz.com/gwprocess/v4/api.php',
                    data=payload,
                    timeout=30
                )
                data = response.json()
                print("SSLCOMMERZ Response:", data)

                if data.get('status') == 'SUCCESS' and data.get('GatewayPageURL'):
                    return redirect(data['GatewayPageURL'])
                else:
                    donation.status = 'FAILED'
                    donation.save()
                    # pass API response to template for debugging
                    return render(request, 'Donation/donate.html', {'form': form, 'error': data.get('failedreason')})

            except Exception as e:
                donation.status = 'FAILED'
                donation.save()
                return render(request, 'Donation/donate.html', {'form': form, 'error': str(e)})
    else:
        form = DonationForm()

    return render(request, 'Donation/donate.html', {'form': form})

# ------------------- IPN Handler -------------------
@csrf_exempt
def ssl_ipn(request):
    val_id = request.POST.get('val_id')
    tran_id = request.POST.get('tran_id')

    if not val_id or not tran_id:
        return HttpResponse("Invalid IPN data")

    validation_url = (
        f"https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php?"
        f"val_id={val_id}&store_id={settings.SSLC_STORE_ID}&store_passwd={settings.SSLC_STORE_PASS}&v=1&format=json"
    )

    res = requests.get(validation_url)
    result = res.json()

    if result and result.get('status') in ['VALID', 'VALIDATED']:
        try:
            donation = Donation.objects.get(order_id=tran_id)
            donation.status = 'PAID'
            donation.val_id = val_id
            donation.save()
        except Donation.DoesNotExist:
            pass
    return HttpResponse("IPN received")

# ------------------- User Donation History -------------------
@login_required
def donation_history(request):
    donations = Donation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'Donation/history.html', {'donations': donations})

# ------------------- Admin Dashboard -------------------
@staff_member_required
def admin_donations(request):
    status_filter = request.GET.get('status')
    donations = Donation.objects.all().order_by('-created_at')
    if status_filter:
        donations = donations.filter(status=status_filter)
    total = donations.filter(status='PAID').aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'Donation/admin_donations.html', {'donations': donations, 'total': total, 'status_filter': status_filter})





@csrf_exempt
def donate_success(request):
    val_id = request.POST.get('val_id')
    tran_id = request.POST.get('tran_id')

    if not val_id or not tran_id:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": False, "error": "Missing transaction data"})
        return HttpResponse("Missing transaction data")

    # Validate with SSLCommerz
    validation_url = (
        f"https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php?"
        f"val_id={val_id}&store_id={settings.SSLC_STORE_ID}&store_passwd={settings.SSLC_STORE_PASS}&v=1&format=json"
    )

    res = requests.get(validation_url)
    result = res.json()

    if result.get('status') in ['VALID', 'VALIDATED']:
        try:
            donation = Donation.objects.get(order_id=tran_id)
            donation.status = 'PAID'
            donation.val_id = val_id
            donation.save()

            # Return JSON if AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "message": "Donation Successful!"})

            return render(request, 'Donation/success.html', {'donation': donation})

        except Donation.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "error": "Donation record not found"})
            return HttpResponse("Donation record not found")
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": False, "error": result.get('error', 'Payment failed')})
        return render(request, 'Donation/fail.html', {'error': result})



def donate_fail(request):
    return render(request, 'Donate/fail.html')

def donate_cancel(request):
    return render(request, 'Donate/cancel.html')

def donation_history_dashboard(request):
    donations = Donation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'Dashboard/dashboard_donation_history.html', {'donations': donations})