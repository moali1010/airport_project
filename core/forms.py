from django import forms
from .models import Flight, Ticket, CartItem


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['flight_number', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'airline',
                  'airplane_type']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_number', 'flight', 'seat', 'agency', 'price', 'status']


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['flight', 'seat']  # agency از کاربر فعلی گرفته می‌شود.
