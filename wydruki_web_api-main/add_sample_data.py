import os
import django

# Ustawienie zmiennej środowiskowej DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magazyn_config.settings')

# Inicjalizacja Django
django.setup()

from panel_wydrukow.models import Pracownicy, Wydruki

def add_sample_data():
    # Dodawanie pracowników
    pracownicy = [
        {
            'imie_pracownika': 'Jan',
            'nazwisko_pracownika': 'Kowalski',
            'dzial': 'Produkcja',
            'identyfikator': 'JAN001'
        },
        {
            'imie_pracownika': 'Anna',
            'nazwisko_pracownika': 'Nowak',
            'dzial': 'Magazyn',
            'identyfikator': 'ANN002'
        },
        {
            'imie_pracownika': 'Piotr',
            'nazwisko_pracownika': 'Wiśniewski',
            'dzial': 'Logistyka',
            'identyfikator': 'PI003'
        }
    ]

    for pracownik in pracownicy:
        Pracownicy.objects.create(**pracownik)

    # Dodawanie produktów
    produkty = [
        {
            'kod': '001',
            'opis': 'Produkt testowy 1',
            'ilosc': 100,
            'szt_w_wor': 10,
            'niski_stan': 20
        },
        {
            'kod': '002',
            'opis': 'Produkt testowy 2',
            'ilosc': 50,
            'szt_w_wor': 5,
            'niski_stan': 10
        },
        {
            'kod': '003',
            'opis': 'Produkt testowy 3',
            'ilosc': 75,
            'szt_w_wor': 15,
            'niski_stan': 15
        },
        {
            'kod': '004',
            'opis': 'Produkt testowy 4',
            'ilosc': 200,
            'szt_w_wor': 20,
            'niski_stan': 30
        }
    ]

    for produkt in produkty:
        Wydruki.objects.create(**produkt)

if __name__ == '__main__':
    print("Dodawanie przykładowych danych...")
    add_sample_data()
    print("Zakończono dodawanie danych.") 