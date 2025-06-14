#!/usr/bin/env python3
import tkinter as tk
from tkinter import font, messagebox
import urllib.request
import io
import os
from PIL import Image, ImageTk

# Kolory systemu
COLORS = {
    'primary': '#2c3e50',      # Ciemny granat
    'secondary': '#3498db',    # Jasny niebieski
    'accent': '#e74c3c',       # Czerwony
    'background': '#ecf0f1',   # Jasny szary
    'text': '#2c3e50',         # Ciemny tekst
    'white': '#ffffff',        # Biały
    'success': '#27ae60',      # Zielony
    'warning': '#f39c12'       # Pomarańczowy
}

class MagazynekUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Magazynek")

        # Konfiguracja pełnoekranowa dla Raspberry Pi
        self.root.attributes('-fullscreen', True)
        
        # Zmienne stanu aplikacji
        self.current_product = None
        self.current_employee = None
        self.first_scan_employee_id = None
        self.quantity = 1
        
        # Konfiguracja czcionek
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=18)
        self.button_font = font.Font(family="Helvetica", size=20, weight="bold")
        
        # Główny kontener
        self.main_frame = tk.Frame(self.root, 
                                bg=COLORS['background'],
                                highlightbackground=COLORS['primary'],
                                highlightthickness=3)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Callback dla zeskanowanych kodów
        self.scan_callback = None

        # Logo
        raw = Image.open('logo.png')
        raw = raw.resize((200, 200), Image.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(raw)

        # Pokaż ekran powitalny
        self.show_welcome_screen()
        self.reset_application()

        # Przycisk wyjścia
        exit_button = tk.Button(self.root, text="Wyjście", command=self.exit_app, 
                               font=self.normal_font, bg=COLORS['accent'], fg=COLORS['white'])
        exit_button.place(x=10, y=10, width=100, height=40)

    def clear_main_frame(self):
        """Czyści główną ramkę."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def add_logo(self):
        """Place the logo immediately under the title."""
        lbl = tk.Label(self.main_frame, image=self.logo_image, bg=COLORS['background'])
        lbl.image = self.logo_image       # reinforce reference
        lbl.pack(pady=(0, 20))            # space after logo

    def show_welcome_screen(self):
        """Wyświetla ekran powitalny."""
        print("=== DEBUG: show_welcome_screen() wywołane ===")
        
        # KLUCZOWE: Resetuj scanner PRZED wyświetleniem ekranu
        if hasattr(self, 'on_scanner_reset_needed'):
            print("DEBUG: Resetowanie skanera przed wyświetleniem welcome screen")
            self.on_scanner_reset_needed()
        else:
            print("DEBUG: Brak callbacku on_scanner_reset_needed!")
        
        self.clear_main_frame()
        
        # Resetujemy zmienne stanu
        self.current_product = None
        self.current_employee = None
        self.first_scan_employee_id = None
        print("DEBUG: Zmienne stanu UI zresetowane")
        
        # Logo i tytuł
        tk.Label(self.main_frame, text="Magazynek Produktów", 
                font=self.title_font, bg=COLORS['background'], fg=COLORS['primary']).pack(pady=40)
        self.add_logo()
        
        # Ramka z instrukcją obsługi
        instruction_frame = tk.Frame(self.main_frame, bg=COLORS['white'], padx=20, pady=15, 
                                   relief="raised", bd=2)
        instruction_frame.pack(fill=tk.X, padx=60, pady=(10, 20))
        
        # Tytuł instrukcji
        tk.Label(instruction_frame, text="Instrukcja obsługi:", 
                font=font.Font(family="Helvetica", size=16, weight="bold"), 
                bg=COLORS['white'], fg=COLORS['primary']).pack(anchor="w", pady=(0, 10))
        
        # Kroki instrukcji
        steps = [
            "1. Zeskanuj swój identyfikator",
            "2. Wybierz produkt i zeskanuj jego kod",
            "3. Aby potwierdzić transakcję zeskanuj ponownie swój identyfikator"
        ]
        
        for step in steps:
            tk.Label(instruction_frame, text=step, 
                    font=font.Font(family="Helvetica", size=14), 
                    bg=COLORS['white'], fg=COLORS['text'], anchor="w").pack(fill=tk.X, pady=2)
        
        # Dodatkowa informacja
        tk.Label(instruction_frame, 
                text="Aby dokonać kolejnej transakcji powtórz wszystkie kroki z nowym produktem.", 
                font=font.Font(family="Helvetica", size=12, slant="italic"),
                bg=COLORS['white'], fg=COLORS['text'], anchor="w").pack(fill=tk.X, pady=(8, 0))
        
        # Instrukcja - pierwszego kroku
        tk.Label(self.main_frame, text="Zeskanuj swój identyfikator, aby rozpocząć", 
                font=self.normal_font, bg=COLORS['background'], fg=COLORS['primary']).pack(pady=20)
        
        # Stan skanowania
        self.scan_state = "initial_employee"
        print(f"DEBUG: Stan skanowania ustawiony na: {self.scan_state}")
        
        # Ustaw callback jeśli istnieje
        if self.scan_callback:
            self.scan_callback(self.process_scan)
            print("DEBUG: Callback skanera ustawiony")

    def get_image_from_url(self, product_code, max_width=400, max_height=300):
        """Pobiera obraz z URL na podstawie kodu produktu."""
        url = f"{os.getenv('MEDIA_SERVER_URL', 'https://localhost')}/media/magazyn/{product_code}.png"
        
        try:
                # Pobierz obraz z URL
                # Wyłącz weryfikację SSL dla self-signed certificate
                import ssl
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                
                with urllib.request.urlopen(url, context=ssl_context) as u:
                        raw_data = u.read()
                # Przetwórz dane obrazu
                image = Image.open(io.BytesIO(raw_data))
                
                # Dostosuj wymiary obrazu, zachowując proporcje
                width, height = image.size
                if width > max_width or height > max_height:
                        ratio = min(max_width/width, max_height/height)
                        new_width = int(width * ratio)
                        new_height = int(height * ratio)
                        image = image.resize((new_width, new_height), Image.LANCZOS)
                        
                # Konwertuj na format Tkinter
                photo = ImageTk.PhotoImage(image)
                return photo
        
        except Exception as e:
                print(f"Błąd podczas pobierania obrazu: {e}")
                return None

    def show_employee_scan_success(self, employee):
        """Wyświetla informację o pomyślnym zeskanowaniu identyfikatora pracownika."""
        print(f"DEBUG: show_employee_scan_success() - {employee['identyfikator']}")
        self.clear_main_frame()
        self.current_employee = employee
        self.first_scan_employee_id = employee['identyfikator']
        
        # Tytuł
        tk.Label(self.main_frame, text=f"Witaj, {employee['imie_pracownika']} {employee['nazwisko_pracownika']}", 
                font=self.title_font, bg=COLORS['background'], fg=COLORS['primary']).pack(pady=20)
        self.add_logo()
        # Instrukcja
        tk.Label(self.main_frame, text="Zeskanuj kod produktu, który chcesz pobrać", 
                font=self.normal_font, bg=COLORS['background'], fg=COLORS['primary']).pack(pady=20)
        
        # Stan skanowania
        self.scan_state = "product"
        print(f"DEBUG: Stan skanowania zmieniony na: {self.scan_state}")

    def show_product_info(self, product):
        """Wyświetla informacje o produkcie."""
        print(f"DEBUG: show_product_info() - {product['kod']}")
        self.clear_main_frame()
        self.current_product = product
        
        # Tytuł
        tk.Label(self.main_frame, text="Informacje o produkcie", 
                font=self.title_font, bg=COLORS['background'], fg=COLORS['primary']).pack(pady=20)
        
        # Dane produktu
        product_frame = tk.Frame(self.main_frame, bg=COLORS['white'], padx=20, pady=20)
        product_frame.pack(fill=tk.X, padx=40, pady=10)
        
        tk.Label(product_frame, text=f"Kod: {product['kod']}", 
                font=self.normal_font, bg=COLORS['white'], fg=COLORS['text'], anchor="w").pack(fill=tk.X, pady=5)
        
        tk.Label(product_frame, text=f"Opis: {product['opis']}", 
                font=self.normal_font, bg=COLORS['white'], fg=COLORS['text'], anchor="w").pack(fill=tk.X, pady=5)
        
        tk.Label(product_frame, text=f"Dostępna ilość woreczków: {product['ilosc']}", 
                font=self.normal_font, bg=COLORS['white'], fg=COLORS['text'], anchor="w").pack(fill=tk.X, pady=5)

        # Instrukcja - prośba o ponowne zeskanowanie identyfikatora w ramce z logo
        instruction_frame = tk.Frame(self.main_frame, bg=COLORS['white'], padx=20, pady=10, relief="raised", bd=3)
        # Zwiększ padx z 40 na większą wartość (np. 80-120)
        instruction_frame.pack(fill=tk.X, padx=60, pady=20)  # lub padx=100, padx=120

        # Kontener dla logo i tekstu obok siebie
        content_frame = tk.Frame(instruction_frame, bg=COLORS['white'])
        content_frame.pack(expand=True)

        # Logo obok instrukcji (większy rozmiar - wielkość ramki)
        try:
        # Załaduj i przeskaluj logo do większego rozmiaru
                import os
                from PIL import Image, ImageTk
                
                logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
                img = Image.open(logo_path)
                # Większe logo - rozmiar dopasowany do wysokości ramki
                img = img.resize((100, 100), Image.LANCZOS)
                large_logo = ImageTk.PhotoImage(img)
                
                logo_label = tk.Label(content_frame, image=large_logo, bg=COLORS['white'])
                logo_label.image = large_logo  # Zachowaj referencję
                logo_label.pack(side=tk.LEFT, padx=(0, 15))
        except Exception as e:
                print(f"Nie udało się załadować logo: {e}")

        # Tekst instrukcji obok logo - większy i czarny
        instruction_text = tk.Label(
        content_frame, 
        text="Zeskanuj swój identyfikator, aby zatwierdzić", 
        font=font.Font(family="Helvetica", size=18, weight="bold"),
        bg=COLORS['white'], 
        fg=COLORS['text']  # Czarny tekst
        )
        instruction_text.pack(side=tk.LEFT, pady=5)

        tk.Label(product_frame, text=f"Sztuk w woreczku: {product['szt_w_wor']}", 
                font=self.normal_font, bg=COLORS['white'], fg=COLORS['text'], anchor="w").pack(fill=tk.X, pady=5)
        
        
        # Pobierz i wyświetl obraz produktu
        product_image = self.get_image_from_url(product['kod'])
        if product_image:
                image_label = tk.Label(self.main_frame, image=product_image, bg=COLORS['white'])
                image_label.image = product_image  # Zachowaj referencję do obrazu
                image_label.pack(pady=20)
        

        
        # Stan skanowania
        self.scan_state = "confirm_employee"
        print(f"DEBUG: Stan skanowania zmieniony na: {self.scan_state}")

    
    def show_employee_info(self, employee):
        """Sprawdza zgodność identyfikatorów i wyświetla ekran potwierdzenia."""
        print(f"DEBUG: show_employee_info() - {employee['identyfikator']}")
        # NOWA WALIDACJA: sprawdzamy, czy identyfikator jest ten sam
        if employee['identyfikator'] != self.first_scan_employee_id:
            self.show_error_screen("Identyfikator nie zgadza się z początkowym! Spróbuj ponownie.")
            return
        
        self.clear_main_frame()
        
        # Tytuł
        tk.Label(self.main_frame, text="Potwierdzenie pobrania", 
                font=self.title_font, bg=COLORS['background'], fg=COLORS['primary']).pack(pady=20)
        
        # Dane produktu i pracownika
        info_frame = tk.Frame(self.main_frame, bg=COLORS['white'], padx=20, pady=20)
        info_frame.pack(fill=tk.X, padx=40, pady=10)
        
        tk.Label(info_frame, text=f"Produkt: {self.current_product['opis']} (Kod: {self.current_product['kod']})", 
                font=self.normal_font, bg=COLORS['white'], fg=COLORS['text'], anchor="w").pack(fill=tk.X, pady=5)
        
        tk.Label(info_frame, text=f"Pracownik: {employee['imie_pracownika']} {employee['nazwisko_pracownika']}", 
                font=self.normal_font, bg=COLORS['white'], fg=COLORS['text'], anchor="w").pack(fill=tk.X, pady=5)
        
        tk.Label(info_frame, text=f"Ilość: {self.quantity}", 
                font=self.normal_font, bg=COLORS['white'], fg=COLORS['text'], anchor="w").pack(fill=tk.X, pady=5)
        
        # Przyciski potwierdzenia
        buttons_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        buttons_frame.pack(pady=30)
        
        tk.Button(buttons_frame, text="Anuluj", command=self.show_welcome_screen, 
                 font=self.button_font, bg=COLORS['accent'], fg=COLORS['white'], width=10).pack(side=tk.LEFT, padx=20)
        
        tk.Button(buttons_frame, text="Potwierdź", command=self.confirm_withdrawal, 
                 font=self.button_font, bg=COLORS['success'], fg=COLORS['white'], width=10).pack(side=tk.LEFT, padx=20)
        
        # Stan skanowania
        self.scan_state = "confirm"
        print(f"DEBUG: Stan skanowania zmieniony na: {self.scan_state}")
    
    def show_success_screen(self, message):
        """Wyświetla ekran sukcesu i automatycznie powraca do ekranu głównego po 5 sekundach."""
        print("DEBUG: show_success_screen() wywołane")
        self.clear_main_frame()

        # Ikona sukcesu
        tk.Label(self.main_frame, text="✓", font=font.Font(family="Helvetica", size=60), 
                fg=COLORS['success'], bg=COLORS['background']).pack(pady=20)

        # Tytuł
        tk.Label(self.main_frame, text="Pobranie zakończone pomyślnie", 
                font=self.title_font, bg=COLORS['background']).pack(pady=10)

        # Ramka z komunikatem
        message_frame = tk.Frame(self.main_frame, bg=COLORS['white'], padx=20, pady=20)
        message_frame.pack(fill=tk.X, padx=40, pady=10)

        # Komunikat - używamy text.split('\n') aby obsłużyć wiele linii
        for line in message.split('\n'):
                tk.Label(message_frame, text=line, 
                        font=self.normal_font, bg=COLORS['white'], fg=COLORS['text'], anchor="w").pack(fill=tk.X, pady=2)

        # Informacja o automatycznym powrocie
        countdown_label = tk.Label(self.main_frame, text="Automatyczny powrót za 5 sekund...", 
                font=self.normal_font, bg=COLORS['background'])
        countdown_label.pack(pady=20)

        # Stan skanowania - ustawiamy na "waiting", żeby ignorować skanowania podczas wyświetlania sukcesu
        self.scan_state = "waiting"
        print(f"DEBUG: Stan skanowania zmieniony na: {self.scan_state}")

        # Automatyczny powrót do ekranu głównego po 5 sekundach
        self.root.after(5000, self.show_welcome_screen)

    
    def show_error_screen(self, message):
        """Wyświetla ekran błędu."""
        print(f"DEBUG: show_error_screen() - {message}")
        self.clear_main_frame()
        
        # Ikona błędu
        tk.Label(self.main_frame, text="✗", font=font.Font(family="Helvetica", size=60), 
                fg=COLORS['warning'], bg=COLORS['background']).pack(pady=20)
        
        # Komunikat
        tk.Label(self.main_frame, text=message, 
                font=self.normal_font, bg=COLORS['background']).pack(pady=20)
        
        # Przycisk powrotu
        tk.Button(self.main_frame, text="Powrót", command=self.show_welcome_screen, 
                 font=self.button_font, bg=COLORS['accent'], fg=COLORS['white'], width=10).pack(pady=30)
    
    def set_scan_callback(self, callback):
        """Ustawia funkcję zwrotną dla zeskanowanych kodów."""
        print("DEBUG: set_scan_callback() wywołane")
        self.scan_callback = callback
        # Aktywuj dla bieżącego stanu
        if self.scan_callback:
            self.scan_callback(self.process_scan)

    def process_scan(self, barcode):
        """Przetwarza zeskanowany kod w zależności od aktualnego stanu aplikacji."""
        print(f"=== DEBUG: process_scan() - barcode='{barcode}', stan='{getattr(self, 'scan_state', 'BRAK')}' ===")
        
        # Sprawdź, czy to kod resetujący "00"
        if barcode == "00":
                print("DEBUG: Zeskanowano kod resetujący (00). Przywracanie stanu początkowego aplikacji.")
                self.reset_application()
                return

        # Ignoruj skanowanie podczas oczekiwania (np. podczas pokazywania ekranu sukcesu)
        if self.scan_state == "waiting":
                print(f"DEBUG: Ignorowanie zeskanowanego kodu podczas oczekiwania: {barcode}")
                return
                
        if self.scan_state == "initial_employee":
                print(f"DEBUG: Przetwarzanie initial_employee: {barcode}")
                # Przekazuje pierwszy identyfikator pracownika do funkcji callback w main.py
                if hasattr(self, 'on_initial_employee_scanned'):
                        self.on_initial_employee_scanned(barcode)
                else:
                        print("DEBUG: BRAK on_initial_employee_scanned callback!")
        
        elif self.scan_state == "product":
                print(f"DEBUG: Przetwarzanie product: {barcode}")
                # Przekazuje produkt do funkcji callback w main.py
                if hasattr(self, 'on_product_scanned'):
                        self.on_product_scanned(barcode)
                else:
                        print("DEBUG: BRAK on_product_scanned callback!")
        
        elif self.scan_state == "confirm_employee":
                print(f"DEBUG: Przetwarzanie confirm_employee: {barcode}")
                # Sprawdź, czy zeskanowany kod jest produktem
                if hasattr(self, 'on_check_if_product'):
                        is_product = self.on_check_if_product(barcode)
                        print(f"DEBUG: is_product = {is_product}")
                if is_product:
                        # Jeśli to produkt, zaktualizuj wybrany produkt
                        if hasattr(self, 'on_product_scanned'):
                                self.on_product_scanned(barcode)
                                return
                
                # Jeśli nie jest produktem, traktuj jako identyfikator pracownika
                if hasattr(self, 'on_confirm_employee_scanned'):
                        self.on_confirm_employee_scanned(barcode)
                else:
                        print("DEBUG: BRAK on_confirm_employee_scanned callback!")

    
    def confirm_withdrawal(self):
        """Potwierdza pobranie produktu."""
        print("DEBUG: confirm_withdrawal() wywołane")
        # Przekazuje potwierdzenie do funkcji callback w main.py
        if hasattr(self, 'on_withdrawal_confirmed'):
            self.on_withdrawal_confirmed(self.current_product, self.current_employee, self.quantity)
    
    def exit_app(self):
        """Zamyka aplikację."""
        if messagebox.askokcancel("Wyjście", "Czy na pewno chcesz zamknąć aplikację?"):
            self.root.destroy()


    def reset_application(self):
        """Resetuje stan aplikacji do początkowego."""
        print("DEBUG: reset_application() wywołane")
        
        # Resetowanie zmiennych stanu
        self.current_product = None
        self.current_employee = None
        self.first_scan_employee_id = None
        self.quantity = 1
        
        # Wyświetl komunikat o zresetowaniu
        self.clear_main_frame()
        
        # Ikona informacyjna
        tk.Label(self.main_frame, text="↻", font=font.Font(family="Helvetica", size=60), 
                fg=COLORS['secondary'], bg=COLORS['background']).pack(pady=20)
        
        # Komunikat
        tk.Label(self.main_frame, text="Aplikacja została zresetowana", 
                font=self.title_font, bg=COLORS['background']).pack(pady=10)
        
        # Ustawienie stanu na "waiting", żeby chwilowo ignorować skanowania
        self.scan_state = "waiting"
        print(f"DEBUG: Stan skanowania ustawiony na: {self.scan_state}")
        
        # Automatyczny powrót do ekranu powitalnego po 2 sekundach
        self.root.after(2000, self.show_welcome_screen)

    def show_network_error_screen(self, message):
        """Wyświetla ekran błędu sieciowego z opcją ponowienia."""
        print(f"DEBUG: show_network_error_screen() - {message}")
        self.clear_main_frame()
        
        # Ikona błędu sieciowego
        tk.Label(self.main_frame, text="📡", font=font.Font(family="Helvetica", size=60),
                 fg=COLORS['warning'], bg=COLORS['background']).pack(pady=20)
        
        # Komunikat
        tk.Label(self.main_frame, text="Błąd połączenia z serwerem",
                 font=self.title_font, bg=COLORS['background']).pack(pady=10)
        
        tk.Label(self.main_frame, text=message,
                 font=self.normal_font, bg=COLORS['background']).pack(pady=20)
        
        # Przyciski
        buttons_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        buttons_frame.pack(pady=30)
        
        tk.Button(buttons_frame, text="Spróbuj ponownie", command=self.retry_connection,
                  font=self.button_font, bg=COLORS['success'], fg=COLORS['white'], width=15).pack(side=tk.LEFT, padx=10)
        
        tk.Button(buttons_frame, text="Powrót", command=self.show_welcome_screen,
                  font=self.button_font, bg=COLORS['accent'], fg=COLORS['white'], width=10).pack(side=tk.LEFT, padx=10)

    def retry_connection(self):
        """Sprawdza ponownie połączenie z API."""
        print("DEBUG: retry_connection() wywołane")
        import api_connector as db_connector
        
        if db_connector.health_check():
            self.show_welcome_screen()
        else:
            self.show_network_error_screen("Nadal brak połączenia z serwerem. Sprawdź konfigurację sieci.")
