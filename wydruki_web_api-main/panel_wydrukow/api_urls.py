# panel_wydrukow/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views



# Router dla ViewSets
router = DefaultRouter()
router.register(r'wydruki', api_views.WydrukiViewSet)
router.register(r'pracownicy', api_views.PracownicyViewSet)
router.register(r'pobrania', api_views.PobraniaViewSet)

app_name = 'api'

urlpatterns = [
    # ViewSets przez router
    path('', include(router.urls)),
    
    # Endpoint dla terminala
    path('terminal/pobranie/', api_views.process_terminal_withdrawal, name='terminal_withdrawal'),
    
    # Pomocnicze endpointy
    path('product/<str:code>/', api_views.get_product_by_code, name='product_by_code'),
    path('employee/<str:identifier>/', api_views.get_employee_by_identifier, name='employee_by_identifier'),
    path('dashboard/stats/', api_views.dashboard_stats, name='dashboard_stats'),
    
    # Autentykacja
    path('auth/', include('rest_framework.urls')),
    path('scan-barcode/', api_views.BarcodeScanView.as_view(), name='scan-barcode'),

]
