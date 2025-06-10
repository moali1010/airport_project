from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Airport(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Agency(models.Model):
    # نماینده یک آژانس توریستی یا فروش بلیط که مسئول مدیریت بلیط و پروازهاست.
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure_airport = models.ForeignKey(
        Airport, related_name='departures', on_delete=models.CASCADE)
    arrival_airport = models.ForeignKey(
        Airport, related_name='arrivals', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airline = models.CharField(max_length=100)
    airplane_type = models.CharField(max_length=50, null=True, blank=True)  # اطلاعات هواپیما

    def __str__(self):
        return f"{self.flight_number}: {self.departure_airport.code} -> {self.arrival_airport.code}"


class Seat(models.Model):
    # هر صندلی در یک پرواز به همراه وضعیت آن (موجود، رزرو شده یا فروخته شده)
    STATUS_CHOICES = [
        ('available', 'موجود'),
        ('reserved', 'رزرو شده'),
        ('sold', 'فروخته شده'),
    ]
    flight = models.ForeignKey(Flight, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    class Meta:
        unique_together = ('flight', 'seat_number')

    def __str__(self):
        return f"{self.seat_number} ({self.get_status_display()})"


class Ticket(models.Model):
    # نمایانگر یک بلیط که توسط آژانس صادر می‌شود.
    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('checked', 'چک شده'),
        ('cancelled', 'کنسل شده'),
    ]
    ticket_number = models.CharField(max_length=20, unique=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"بلیط {self.ticket_number} برای پرواز {self.flight.flight_number}"


class CartItem(models.Model):
    # یک آیتم سبد خرید شامل انتخاب یک صندلی برای یک پرواز است.
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"آیتم سبد خرید: پرواز {self.flight.flight_number} - صندلی {self.seat.seat_number}"
