from rest_framework import routers
from django.urls import path, include
from .api_views import AirportViewSet, AgencyViewSet, FlightViewSet, SeatViewSet, TicketViewSet, CartItemViewSet

router = routers.DefaultRouter()
router.register(r'airports', AirportViewSet)
router.register(r'agencies', AgencyViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'cart-items', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
