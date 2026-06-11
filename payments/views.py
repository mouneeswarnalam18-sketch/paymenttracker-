from django.db.models import Q
from django.shortcuts import render
from .models import Customer,Payment
from django.shortcuts import get_object_or_404, redirect
from datetime import date
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
def delete_customer(request, id):

    customer = get_object_or_404(Customer, id=id)

    customer.delete()

    return redirect('customers')
def edit_customer(request, id):

    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":

        customer.customer_code = request.POST['customer_code']
        customer.name = request.POST['name']
        customer.phone = request.POST['phone']

        customer.save()

        return redirect('customers')

    return render(
        request,
        'edit_customer.html',
        {
            'customer': customer
        }
    )
def customers(request):

    query = request.GET.get('q')

    customers = Customer.objects.all()

    if query:
        customers = customers.filter(
            Q(customer_code__icontains=query) |
            Q(name__icontains=query) |
            Q(phone__icontains=query)
        )

    return render(
        request,
        'customers.html',
        {
            'customers': customers
        }
    )
def mark_paid(request, payment_id):

    payment = get_object_or_404(
        Payment,
        id=payment_id
    )

    payment.status = 'Paid'

    payment.paid_date = timezone.now().date()

    payment.paid_time = timezone.now()

    payment.save()

    return redirect('unpaid')
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

def mark_paid(request, payment_id):

    payment = get_object_or_404(Payment, id=payment_id)

    if payment.status != 'Paid':
        payment.status = 'Paid'
        payment.paid_date = timezone.now().date()
        payment.paid_time = timezone.now()
        payment.save()

    return redirect('unpaid')
def search_customer(request):
    query = request.GET.get('q')

    if query:
        customers = Customer.objects.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(customer_code__icontains=query)
        )
    else:
        customers = []

    return render(
        request,
        'search.html',
        {'customers': customers}

    )
def payment_history(request):
    query = request.GET.get('q')

    customer = None
    payments = []

    if query:
        customer = Customer.objects.filter(
            Q(customer_code__icontains=query) |
            Q(name__icontains=query) |
            Q(phone__icontains=query)
        ).first()

        if customer:
            payments = Payment.objects.filter(
                customer=customer
            ).order_by('year', 'month')

    return render(
        request,
        'payment_history.html',
        {
            'customer': customer,
            'payments': payments
        }
    )
def dashboard(request):

    today = date.today()

    current_month = today.month
    current_year = today.year

    total_customers = Customer.objects.count()

    monthly_payments = Payment.objects.filter(
        month=current_month,
        year=current_year
    )

    paid_count = monthly_payments.filter(
        status='Paid'
    ).count()

    unpaid_count = monthly_payments.filter(
        status='Not Paid'
    ).count()

    expected_collection = total_customers * 3000

    received_collection = paid_count * 3000

    pending_collection = expected_collection - received_collection

    return render(
        request,
        'dashboard.html',
        {
            'total_customers': total_customers,
            'paid_count': paid_count,
            'unpaid_count': unpaid_count,
            'expected_collection': expected_collection,
            'received_collection': received_collection,
            'pending_collection': pending_collection,
            'current_month': current_month,
            'current_year': current_year,
        }
    )
from django.db.models import Q
from datetime import date

def unpaid_customers(request):

    today = date.today()

    current_month = today.month
    current_year = today.year

    query = request.GET.get('q')

    payments = Payment.objects.filter(
        status='Not Paid',
        month=current_month,
        year=current_year
    )

    if query:
        payments = payments.filter(
            Q(customer__customer_code__icontains=query) |
            Q(customer__name__icontains=query) |
            Q(customer__phone__icontains=query)
        )
        print("SEARCH =", query)
        print("RESULTS =", payments.count())
    return render(
        request,
        'unpaid_customers.html',
        {
            'payments': payments,
            'current_month': current_month,
            'current_year': current_year
        }
    )