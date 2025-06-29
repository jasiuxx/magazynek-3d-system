# panel_wydrukow/serializers.py
from rest_framework import serializers
from .models import Wydruki, Pobrania, Pracownicy

class WydrukiSerializer(serializers.ModelSerializer):
    stan_calkowity = serializers.ReadOnlyField()
    ma_niski_stan = serializers.ReadOnlyField()
    
    class Meta:
        model = Wydruki
        fields = ['id', 'kod', 'opis', 'ilosc', 'szt_w_wor', 
                 'niski_stan', 'stan_calkowity', 'ma_niski_stan']
        
    def validate_kod(self, value):
        """Walidacja unikalności kodu podczas edycji przez API."""
        if self.instance and self.instance.kod == value:
            return value  # Bez zmian - OK
            
        if Wydruki.objects.filter(kod=value).exists():
            raise serializers.ValidationError("Produkt o takim kodzie już istnieje.")
        return value

class PracownicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pracownicy
        fields = ['pracownicy_id', 'imie_pracownika', 'nazwisko_pracownika',
                 'dzial', 'identyfikator']
        
class PobraniaSerializer(serializers.ModelSerializer):
    wydruk_kod = serializers.CharField(source='wydruk.kod', read_only=True)
    wydruk_opis = serializers.CharField(source='wydruk.opis', read_only=True)
    pracownik_imie = serializers.CharField(source='identyfikator.imie_pracownika', read_only=True)
    pracownik_nazwisko = serializers.CharField(source='identyfikator.nazwisko_pracownika', read_only=True)
    
    class Meta:
        model = Pobrania
        fields = ['id', 'wydruk', 'wydruk_kod', 'wydruk_opis',
                 'identyfikator', 'pracownik_imie', 'pracownik_nazwisko',
                 'imie_pracownika', 'nazwisko_pracownika',
                 'ilosc', 'data_pobrania']

class PobranieTerminalSerializer(serializers.Serializer):
    """Serializer dla operacji pobrania z terminala."""
    product_code = serializers.CharField(max_length=50)
    employee_identifier = serializers.CharField(max_length=30)
    quantity = serializers.IntegerField(min_value=1, default=1)
    
    def validate_product_code(self, value):
        """Sprawdza czy produkt istnieje."""
        try:
            product = Wydruki.objects.get(kod=value)
            return value
        except Wydruki.DoesNotExist:
            raise serializers.ValidationError("Produkt nie znaleziony.")
    
    def validate_employee_identifier(self, value):
        """Sprawdza czy pracownik istnieje."""
        try:
            employee = Pracownicy.objects.get(identyfikator=value)
            return value
        except Pracownicy.DoesNotExist:
            raise serializers.ValidationError("Pracownik nie znaleziony.")
