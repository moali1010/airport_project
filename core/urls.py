from django.urls import path
from .views import (
    FlightSearchView,
    seat_map_view,
    CartView,
    add_to_cart_view,
    checkout_view,
    TicketHistoryView,
    FlightCreateView,
)

urlpatterns = [
    path('flights/search/', FlightSearchView.as_view(), name='flight_search'),
    path('flight/<int:flight_id>/seats/', seat_map_view, name='seat_map'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:flight_id>/<int:seat_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/checkout/', checkout_view, name='checkout'),
    path('tickets/history/', TicketHistoryView.as_view(), name='ticket_history'),
    path('agencies/flight/create/', FlightCreateView.as_view(), name='flight_create'),
]
