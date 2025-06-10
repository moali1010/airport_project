from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from .models import Flight, Seat, CartItem, Ticket, Agency, Airport
from .forms import FlightForm


# Create your views here.
# ویوی جستجو بر اساس فرودگاه مبدأ و مقصد
class FlightSearchView(ListView):
    model = Flight
    template_name = 'flight_search.html'
    context_object_name = 'flights'

    def get_queryset(self):
        queryset = super().get_queryset()
        dep_airport = self.request.GET.get('departure')
        arr_airport = self.request.GET.get('arrival')
        if dep_airport:
            queryset = queryset.filter(departure_airport__code=dep_airport)
        if arr_airport:
            queryset = queryset.filter(arrival_airport__code=arr_airport)
        # نمایش تنها پروازهای آینده
        queryset = queryset.filter(departure_time__gte=timezone.now())
        return queryset


# نمایش گرافیکی نقشه صندلی‌های یک پرواز
def seat_map_view(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    seats = flight.seats.all().order_by('seat_number')
    context = {
        'flight': flight,
        'seats': seats,
    }
    return render(request, 'seat_map.html', context)


# نمایش سبد خرید
@method_decorator(login_required, name='dispatch')
class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agency = get_object_or_404(Agency, user=self.request.user)
        cart_items = CartItem.objects.filter(agency=agency)
        context['cart_items'] = cart_items
        return context


# افزودن یک صندلی به سبد خرید (انتخاب صندلی)
@login_required
def add_to_cart_view(request, flight_id, seat_id):
    agency = get_object_or_404(Agency, user=request.user)
    flight = get_object_or_404(Flight, id=flight_id)
    seat = get_object_or_404(Seat, id=seat_id, flight=flight, status='available')
    # ایجاد یا گرفتن آیتم موجود در سبد خرید
    cart_item, created = CartItem.objects.get_or_create(agency=agency, flight=flight, seat=seat)
    # به عنوان نمونه، وضعیت صندلی را به "رزرو شده" تغییر می‌دهیم.
    seat.status = 'reserved'
    seat.save()
    return redirect('cart')


# تکمیل خرید؛ تبدیل آیتم‌های سبد خرید به بلیط‌های نهایی
@login_required
def checkout_view(request):
    agency = get_object_or_404(Agency, user=request.user)
    cart_items = CartItem.objects.filter(agency=agency)
    for item in cart_items:
        ticket_number = f"TICKET-{item.flight.flight_number}-{item.seat.seat_number}"
        Ticket.objects.create(
            ticket_number=ticket_number,
            flight=item.flight,
            seat=item.seat,
            agency=agency,
            price=100.00,  # قیمت نمونه؛ در پروژه واقعی می‌توان قیمت داینامیک داشت.
            status='active'
        )
        # تغییر وضعیت صندلی به فروخته شده
        item.seat.status = 'sold'
        item.seat.save()
        item.delete()
    return redirect('ticket_history')


# نمایش تاریخچه بلیط‌های خریداری شده (پروازهای گذشته)
@method_decorator(login_required, name='dispatch')
class TicketHistoryView(ListView):
    model = Ticket
    template_name = 'ticket_history.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        agency = get_object_or_404(Agency, user=self.request.user)
        return Ticket.objects.filter(agency=agency).order_by('-purchase_date')


# ویوی ایجاد پرواز برای اژانس‌ها
@method_decorator(login_required, name='dispatch')
class FlightCreateView(CreateView):
    model = Flight
    form_class = FlightForm
    template_name = 'flight_form.html'
    success_url = '/'

    def form_valid(self, form):
        # در صورت نیاز، می‌توان بررسی‌های مجوزی نیز اضافه کرد.
        return super().form_valid(form)
