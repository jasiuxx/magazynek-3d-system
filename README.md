
[🇬🇧 Read in English](README-EN.md)

# Magazyn 360

Kompletny system do zarządzania magazynem składający się z aplikacji terminalowej (Raspberry Pi) oraz systemu webowego (Django) do administracji magazynem.

text
---

## 🏗️ Architektura systemu

### **🖥️ Aplikacja terminala magazynowego (Raspberry Pi)**
- **Urządzenie:** Raspberry Pi 4 z ekranem dotykowym
- **Interfejs:** Python Tkinter w trybie pełnoekranowym
- **Skanowanie:** Fizyczne skanery USB (evdev) + obsługa kodów kreskowych lub skaner mobilny w telefonie
- **Przeznaczenie:** Terminal dla pracowników pobierających produkty z magazynu

### **🌐 System webowy Django**
- **Backend:** Django REST Framework
- **Frontend:** Panel administracyjny + interfejs HTML5 do skanowania mobilnego
- **API:** REST endpoints z autoryzacją tokenami
- **Przeznaczenie:** Zarządzanie magazynem, produktami, pobraniami


### **📷 Serwer obrazów produktów**
- **Serwer:** Apache/nginx na dedykowanym urządzeniu 
- **Protokół:** HTTPS z self-signed certificate dla sieci lokalnej
- **Struktura:** `/wydruki/{kod_produktu}.png` - automatyczne mapowanie kodów na pliki
- **Integracja:** Automatyczne wyświetlanie zdjęć produktów w interfejsie terminala
- System webowy podczas tworzenia nowego produktu przesyła wgrane zdjęcie na serwer apache i jednocześnie zmienia format na .png oraz wymiary na 400x400
- Dzięki temu podczas obsługi produktów widać ich obraz


---

## 🔄 Przepływ operacji magazynowej

### **Workflow na terminalu Raspberry Pi:**
1. **Autoryzacja:** Pracownik skanuje swój identyfikator
2. **Wybór produktu:** Skanowanie kodu kreskowego produktu
3. **Potwierdzenie:** Ponowne skanowanie identyfikatora pracownika
4. **Rejestracja:** System automatycznie rejestruje pobranie w bazie Django

### **Zarządzanie przez system webowy:**
- Dodawanie/edycja produktów i pracowników
- Śledzenie stanów magazynowych w czasie rzeczywistym
- Historia pobrań i raportowanie
- Skanowanie mobilne przez przeglądarkę (HTML5)

---

## 📁 Struktura projektu
```

magazynek-3d-system/
├── raspberry-pi-terminal/        # Aplikacja terminala (Raspberry Pi)
│   ├── main.py                   # Główna logika aplikacji
│   ├── ui_manager.py             # Interfejs graficzny Tkinter
│   ├── barcode_scanner.py        # Obsługa skanera USB
│   ├── api_connector.py          # Komunikacja z Django API
│   ├── logo.png                  # Logo 
│   └── requirements.txt          # Zależności Python
│
├── django-backend/               # System webowy (Django)
│   ├── wydruki_web_api/          # Główny projekt Django
│   │   ├── settings.py           # Ustawienia Django
│   │   ├── urls.py               # Konfiguracja URL-i
│   │   └── wsgi.py               # Punkt wejściowy WSGI
│   ├── panel_wydrukow/           # Aplikacja magazynowa
│   │   ├── models.py             # Modele: produkty, pracownicy, pobrania
│   │   ├── views.py              # Widoki API i webowe
│   │   ├── templates/            # Szablony HTML
│   │   │   └── scan.html         # Strona skanowania mobilnego
│   │   └── static/               # Pliki statyczne (CSS, JS, obrazy)
│   └── requirements.txt          # Zależności Python dla Django
│
├── media-server/                 # Serwer obrazów 
│   ├── apache-config/            # Konfiguracja Apache HTTPS
│   └── wydruki/                  # Katalog zdjęć produktów
│       ├── PROD_001.png          # Zdjęcie produktu PROD_001
│       ├── FRAME_002.png         # Zdjęcie produktu FRAME_002
│       └── ...                   # Inne zdjęcia produktów
│
├── README-PL.md                  # Dokumentacja po polsku
├── README-EN.md                  # Dokumentacja po angielsku
└── .env.example                  # Szablon zmiennych środowiskowych

```

text

---

## ⚙️ Funkcjonalności aplikacji terminalowej

### **Interfejs użytkownika:**
- **Ekran powitalny** z instrukcją obsługi krok po kroku
- **Automatyczne wykrywanie skanera** USB z filtrowaniem urządzeń
- **Wyświetlanie zdjęć produktów** pobieranych z serwera mediów
- **Walidacja dwuetapowa** identyfikatora pracownika
- **Obsługa błędów** z komunikatami w języku polskim
- **Reset aplikacji** kodem specjalnym "00"

### **Komponenty techniczne:**
- `main.py` – orchestracja aplikacji i logika biznesowa
- `ui_manager.py` – interfejs graficzny z ekranami stanu
- `barcode_scanner.py` – obsługa skanera z mapowaniem kodów ASCII
-  `api_barcode_scanner.py` – obsługa skanera z przeglądaki
- `api_connector.py` – komunikacja REST API z cache'owaniem

---

## 🌐 System webowy Django

### **REST API Endpoints:**
POST /api/scan-barcode/ # Zapis kodu z skanowania mobilnego
GET /api/product/<kod>/ # Informacje o produkcie
GET /api/employee/<id>/ # Dane pracownika
POST /api/terminal/pobranie/ # Rejestracja pobrania produktu
GET /api/dashboard/stats/ # Statystyki systemu (healthcheck)

text

### **Autoryzacja:**
Wszystkie endpointy wymagają nagłówka:
Authorization: Token <twój_token>

text

### **Panel administracyjny:**
- Zarządzanie produktami 
- Historia pobrań z datami i ilościami
- Zarządzanie stanami magazynowymi( dodawanie,usuwanie,edycja)




## 📱 Skanowanie mobilne

System obsługuje również skanowanie przez przeglądarkę mobilną:
- **URL:** `https://your-server:8000/scan/`
- **Technologia:** HTML5 + ZXing-js
- **Wsparcie:** iOS Safari, Android Chrome
- **Funkcje:** Wybór kamery, celownik, obsługa błędów


## 📸 Zrzuty ekranu

System zawiera następujące ekrany:
- **Ekran powitalny** z instrukcją obsługi
  
  <img width="699" alt="image" src="https://github.com/user-attachments/assets/820b1171-18cf-42d9-bbf9-b0eb3ede15e4" />
- **Skanowanie przez przeglądarę**

  ![image](https://github.com/user-attachments/assets/c68b124b-475b-46bf-9de2-c6bf0b72c5a6)

  
- **Potwierdzenie identyfikatora** pracownika

  <img width="701" alt="image" src="https://github.com/user-attachments/assets/f2b7c8a8-ae0e-4283-9e3a-0d19c539a4dd" />


- **Skanowanie produktu

  ![image](https://github.com/user-attachments/assets/20c9d9a0-4b9c-4a9f-b88f-78bde61911f9)

  
- **Informacje o produkcie** ze zdjęciem

  <img width="704" alt="image" src="https://github.com/user-attachments/assets/593fc68c-8265-4276-a27e-ce90eab2ded2" />

- **Potwierdzenie kodu oraz Ekran sukcesu** po potwierdzeniu transakcji

  <img width="697" alt="image" src="https://github.com/user-attachments/assets/f49b7014-a46c-46bb-a973-1a4a074eb1d6" />

- **Obsługa błędów** z jasnymi komunikatami

  <img width="700" alt="image" src="https://github.com/user-attachments/assets/7db2f601-a8e4-421e-9527-51dcf06565f9" />

  <img width="701" alt="image" src="https://github.com/user-attachments/assets/295cc931-86af-42c2-bf18-23229713499a" />

# Widok webowego systemu

- **Pobranie zarejestrowane w bazie**

  ![image](https://github.com/user-attachments/assets/f619868e-6274-4b4c-8f46-0c2e7f7a0782)

  <img width="670" alt="image" src="https://github.com/user-attachments/assets/2469f3bc-6769-4e09-974c-5cd441e007e5" />


- **Dashboard**

  ![image](https://github.com/user-attachments/assets/b41a67fe-c248-4705-a1dd-bff8fe364fa5)

- **Lista produktów**

![image](https://github.com/user-attachments/assets/43d203a4-a9e7-409c-b1ec-33ec621b0776)


- **Dodawanie/edycja produktu**


![image](https://github.com/user-attachments/assets/b4b5b546-32e4-458c-bac7-2f7cb75d850b)

- **Serwer ze zdjeciami**

<img width="451" alt="image" src="https://github.com/user-attachments/assets/9d6d9b23-93a5-45ef-b381-5d32eade06ef" />


# Kierunek rozwoju:
Chcę się skupić na rozwoju panelu administratora w Django ,aby szef magazynu mógł dostosowywać funkcję pod siebie. Chciałbym aby magazyn 360 był jak najbardziej uniwersalny pod potrzeby klientów.


---



## 📄 Licencja


### Użycie niekomercyjne
Kod dostępny jest do wglądu w celach:
- Edukacyjnych i naukowych
- Prezentacji umiejętności programistycznych
- Analizy rozwiązań technicznych

### Użycie komercyjne
Wykorzystanie komercyjne wymaga pisemnej zgody autora.

### Commercial Licensing
Commercial use requires written permission. 


