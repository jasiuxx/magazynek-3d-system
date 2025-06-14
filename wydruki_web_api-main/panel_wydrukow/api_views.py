# panel_wydrukow/api_views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone

from .models import Wydruki, Pobrania, Pracownicy
from .serializers import (
    WydrukiSerializer, PobraniaSerializer, PracownicySerializer,
    PobranieTerminalSerializer
)

class WydrukiViewSet(viewsets.ModelViewSet):
    """ViewSet dla zarządzania produktami."""
    queryset = Wydruki.objects.all()
    serializer_class = WydrukiSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrowanie i wyszukiwanie produktów."""
        queryset = Wydruki.objects.all()
        search = self.request.query_params.get('search', None)
        kod = self.request.query_params.get('kod', None)
        
        if search:
            queryset = queryset.filter(
                models.Q(kod__icontains=search) | 
                models.Q(opis__icontains=search)
            )
        
        if kod:
            queryset = queryset.filter(kod=kod)
            
        return queryset.order_by('kod')
    
    @action(detail=False, methods=['get'])
    def niski_stan(self, request):
        """Endpoint dla produktów z niskim stanem."""
        from django.db.models import F
        niski_stan_produkty = Wydruki.objects.filter(ilosc__lt=F('niski_stan'))
        serializer = self.get_serializer(niski_stan_produkty, many=True)
        return Response(serializer.data)

class PracownicyViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet dla pracowników (tylko odczyt)."""
    queryset = Pracownicy.objects.all()
    serializer_class = PracownicySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrowanie pracowników."""
        queryset = Pracownicy.objects.all()
        identyfikator = self.request.query_params.get('identyfikator', None)
        
        if identyfikator:
            queryset = queryset.filter(identyfikator=identyfikator)
            
        return queryset

class PobraniaViewSet(viewsets.ModelViewSet):
    """ViewSet dla historii pobrań."""
    queryset = Pobrania.objects.all()
    serializer_class = PobraniaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrowanie historii pobrań."""
        queryset = Pobrania.objects.all().order_by('-data_pobrania')
        wydruk_id = self.request.query_params.get('wydruk', None)
        pracownik_id = self.request.query_params.get('pracownik', None)
        
        if wydruk_id:
            queryset = queryset.filter(wydruk_id=wydruk_id)
        if pracownik_id:
            queryset = queryset.filter(identyfikator=pracownik_id)
            
        return queryset

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def process_terminal_withdrawal(request):
    """
    Endpoint dla przetwarzania pobrania z terminala.
    Odpowiednik funkcji process_withdrawal z db_connector.py
    """
    serializer = PobranieTerminalSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Błędne dane wejściowe',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    product_code = serializer.validated_data['product_code']
    employee_identifier = serializer.validated_data['employee_identifier']
    quantity = serializer.validated_data['quantity']
    
    try:
        with transaction.atomic():
            # Pobierz produkt
            try:
                product = Wydruki.objects.select_for_update().get(kod=product_code)
            except Wydruki.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Produkt nie znaleziony'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Pobierz pracownika
            try:
                employee = Pracownicy.objects.get(identyfikator=employee_identifier)
            except Pracownicy.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Pracownik nie znaleziony'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Sprawdź dostępność
            if product.ilosc < quantity:
                return Response({
                    'success': False,
                    'message': 'Niewystarczająca ilość produktu'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Zaktualizuj stan produktu
            product.ilosc -= quantity
            product.save()
            
            # Zarejestruj pobranie
            pobranie = Pobrania.objects.create(
                wydruk=product,
                identyfikator=employee,
                imie_pracownika=employee.imie_pracownika,
                nazwisko_pracownika=employee.nazwisko_pracownika,
                ilosc=quantity
            )
            
            return Response({
                'success': True,
                'message': 'Pobranie zarejestrowane pomyślnie',
                'withdrawal_id': pobranie.id,
                'product': {
                    'id': product.id,
                    'kod': product.kod,
                    'opis': product.opis,
                    'ilosc': product.ilosc,
                    'szt_w_wor': product.szt_w_wor
                },
                'employee': {
                    'identyfikator': employee.identyfikator,
                    'imie_pracownika': employee.imie_pracownika,
                    'nazwisko_pracownika': employee.nazwisko_pracownika
                },
                'quantity': quantity
            })
            
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Błąd serwera: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Pomocnicze endpointy dla terminala
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_product_by_code(request, code):
    """Endpoint dla pobierania produktu po kodzie."""
    try:
        product = Wydruki.objects.get(kod=code)
        serializer = WydrukiSerializer(product)
        return Response(serializer.data)
    except Wydruki.DoesNotExist:
        return Response({
            'error': 'Produkt nie znaleziony'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_employee_by_identifier(request, identifier):
    """Endpoint dla pobierania pracownika po identyfikatorze."""
    try:
        employee = Pracownicy.objects.get(identyfikator=identifier)
        serializer = PracownicySerializer(employee)
        return Response(serializer.data)
    except Pracownicy.DoesNotExist:
        return Response({
            'error': 'Pracownik nie znaleziony'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Endpoint z statystykami dla dashboardu."""
    from django.db.models import Sum, F, Q
    from datetime import datetime, time
    
    # Statystyki podstawowe
    wszystkie_wydruki = Wydruki.objects.count()
    niski_stan_count = Wydruki.objects.filter(ilosc__lt=F('niski_stan')).count()
    
    # Dzisiejsze pobrania
    today = timezone.now().date()
    today_start = datetime.combine(today, time.min)
    today_end = datetime.combine(today, time.max)
    
    dzisiejsze_pobrania = Pobrania.objects.filter(
        data_pobrania__range=(today_start, today_end)
    ).count()
    
    # Najpopularniejsze produkty
    popularne_wydruki = Pobrania.objects.values(
        'wydruk__kod', 'wydruk__opis'
    ).annotate(
        total=Sum('ilosc')
    ).order_by('-total')[:5]
    
    return Response({
        'wszystkie_wydruki': wszystkie_wydruki,
        'niski_stan': niski_stan_count,
        'dzisiejsze_pobrania': dzisiejsze_pobrania,
        'popularne_wydruki': list(popularne_wydruki)
    })




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

LAST_BARCODE = {"barcode": None}
class BarcodeScanView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        global LAST_BARCODE 
        barcode = request.data.get('barcode')
        if barcode:
            LAST_BARCODE["barcode"] = barcode
            return Response({"message": "Kod zapisany"}, status=status.HTTP_200_OK)
        return Response({"error": "Brak kodu"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        global LAST_BARCODE
        barcode = LAST_BARCODE["barcode"]
        LAST_BARCODE = {"barcode": None}
        return Response({"barcode": barcode}, status=status.HTTP_200_OK)

