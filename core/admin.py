from django.contrib import admin
from .models import Airport, Agency, Flight, Seat, Ticket, CartItem


# Register your models here.
@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'city', 'country']
    search_fields = ['name', 'code']


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'contact_email', 'contact_phone']
    search_fields = ['name', 'user__username']


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['flight_number', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time',
                    'airline']
    list_filter = ['airline', 'departure_airport', 'arrival_airport']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['seat_number', 'flight', 'status']
    list_filter = ['status', 'flight']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'flight', 'seat', 'agency', 'price', 'status', 'purchase_date']
    list_filter = ['status', 'agency']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['agency', 'flight', 'seat', 'added_at']
