# Magazynek 3D - System zarządzania wydrukami

System do zarządzania magazynem wydruków 3D z interfejsem Tkinter i integracją z Django REST API.

## 🔧 Technologie

- **Backend:** Python, Django REST Framework
- **Frontend:** Tkinter (desktop GUI)
- **Baza danych:** MySQL/PostgreSQL
- **Skanowanie:** evdev, USB barcode scanners
- **API:** REST, Token authentication
- **Deployment:** Raspberry Pi 4

## ⚙️ Funkcjonalności

- Skanowanie kodów kreskowych (USB/mobilna kamera)
- Autoryzacja dwuetapowa (pracownik → produkt → potwierdzenie)
- Wyświetlanie zdjęć produktów
- Rejestracja pobrań w czasie rzeczywistym
- Cache'owanie danych API
- Obsługa błędów sieciowych



## 📁 Struktura projektu

- `main.py` - Główna logika aplikacji
- `ui_manager.py` - Interfejs użytkownika Tkinter
- `barcode_scanner.py` - Obsługa skanera USB
- `api_barcode_scanner.py` - Obsługa skanera na telefonie
- `api_connector.py` - Komunikacja z Django API
- `requirements.txt` - Zależności Python

## 🛡️ Bezpieczeństwo

- Tokeny API przechowywane w zmiennych środowiskowych
- Autoryzacja dwuetapowa użytkowników
- Walidacja danych wejściowych
- Obsługa self-signed SSL certificates

## 📸 Screenshots

*Dodaj tutaj zrzuty ekranu aplikacji*

## 🤝 Kontakt

Projekt stworzony jako część portfolia programistycznego.
