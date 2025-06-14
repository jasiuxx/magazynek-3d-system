from django.urls import path
from . import views
from .views import BarcodeScanPageView

app_name = 'panel_wydrukow'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('wydruki/', views.lista_wydrukow, name='lista_wydrukow'),
    path('wydruki/dodaj/', views.dodaj_wydruk, name='dodaj_wydruk'),
    path('wydruki/edytuj/<int:id>/', views.edytuj_wydruk, name='edytuj_wydruk'),
    path('pobrania/', views.historia_pobran, name='historia_pobran'),
    path('wydruki/usun/<int:id>/', views.usun_wydruk, name='usun_wydruk'),
    path('historia/cofnij/<int:pobranie_id>/', views.cofnij_pobranie, name='cofnij_pobranie'),
    path('temp-stock/', views.temp_stock_view, name='temp_stock_view'),
    path('scan/', BarcodeScanPageView.as_view(), name='barcode_scan_page'),
]
