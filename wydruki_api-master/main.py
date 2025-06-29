#!/usr/bin/env python3
import tkinter as tk
import sys
import time
import signal
import threading
import queue
import socket

# Importuj własne moduły
from api_barcode_scanner import APIBarcodeScanner as BarcodeScanner
from ui_manager import MagazynekUI
import api_connector as db_connector

class MagazynekApp:
    def __init__(self):
        # Inicjalizacja głównego okna Tkinter
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Inicjalizacja interfejsu użytkownika
        self.ui = MagazynekUI(self.root)
        
        # Podłączenie funkcji zwrotnych UI
        self.ui.on_initial_employee_scanned = self.handle_initial_employee_scan
        self.ui.on_product_scanned = self.handle_product_scan
        self.ui.on_confirm_employee_scanned = self.handle_confirm_employee_scan
        self.ui.on_withdrawal_confirmed = self.handle_withdrawal_confirmation
        self.ui.on_check_if_product = self.check_if_product
        # KLUCZOWE: Dodanie callbacku resetowania skanera
        self.ui.on_scanner_reset_needed = self.reset_scanner_after_waiting
        
        if not db_connector.health_check():
            self.ui.show_error_screen("Brak połączenia z serwerem! Sprawdź sieć i spróbuj ponownie.")
            return

        # Inicjalizacja skanera kodów kreskowych
        self.scanner = BarcodeScanner(api_url="https://ADRES/api/scan-barcode/")
        
        # Podłączenie skanera do UI
        self.ui.set_scan_callback(self.set_scanner_callback)
        
        # Uruchomienie skanera
        self.scanner.start_scanning()
        
        # Obsługa sygnału zamknięcia
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Kolejka dla kodów z symulatora
        self.barcode_queue = queue.Queue()
        self.start_barcode_processor()
        
        # Uruchomienie serwera gniazda
        self.start_socket_server()
    
    def start_socket_server(self):
        """Uruchamia serwer gniazda do komunikacji z symulatorem."""
        def run_server():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('localhost', 12345))
            server.listen(1)
            
            while True:
                try:
                    client, addr = server.accept()
                    print(f"Połączono z symulatorem: {addr}")
                    
                    while True:
                        data = client.recv(1024)
                        if not data:
                            break
                            
                        # Przetwórz otrzymane kody
                        codes = data.decode().strip().split('\n')
                        for code in codes:
                            if code:
                                self.add_barcode(code)
                                
                except Exception as e:
                    print(f"Błąd serwera gniazda: {e}")
                finally:
                    try:
                        client.close()
                    except:
                        pass
        
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
    
    def start_barcode_processor(self):
        """Uruchamia wątek przetwarzający kody z symulatora."""
        def process_queue():
            while True:
                try:
                    barcode = self.barcode_queue.get(timeout=0.1)
                    # Przetwórz kod w głównym wątku
                    self.root.after(0, self.process_barcode, barcode)
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Błąd przetwarzania kodu: {e}")
        
        thread = threading.Thread(target=process_queue, daemon=True)
        thread.start()
    
    def process_barcode(self, barcode):
        """Przetwarza kod kreskowy z symulatora."""
        if hasattr(self.ui, 'scan_state'):
            if self.ui.scan_state == "initial_employee":
                self.handle_initial_employee_scan(barcode)
            elif self.ui.scan_state == "product":
                self.handle_product_scan(barcode)
            elif self.ui.scan_state == "confirm_employee":
                self.handle_confirm_employee_scan(barcode)
    
    def add_barcode(self, barcode):
        """Dodaje kod do kolejki przetwarzania."""
        self.barcode_queue.put(barcode)
    
    def set_scanner_callback(self, callback):
        """Ustawia funkcję zwrotną dla skanera."""
        self.scanner.register_callback(callback)
    
    def handle_initial_employee_scan(self, barcode):
        """Obsługuje pierwsze skanowanie identyfikatora pracownika."""
        print(f"DEBUG: handle_initial_employee_scan() - {barcode}")
        
        # Pobierz informacje o pracowniku z bazy danych
        employee = db_connector.get_employee_by_identifier(barcode)
        
        if employee:
            self.ui.show_employee_scan_success(employee)
        else:
            self.ui.show_error_screen(f"Nie znaleziono pracownika o identyfikatorze: {barcode}")
    
    def handle_product_scan(self, barcode):
        """Obsługuje zeskanowanie kodu produktu."""
        # Konwersja myślników na podkreślenia
        barcode = barcode.replace("-", "_")
        print(f"DEBUG: handle_product_scan() - {barcode}")
        
        # Pobierz informacje o produkcie z bazy danych
        product = db_connector.get_product_by_code(barcode)
        
        if product:
            self.ui.show_product_info(product)
        else:
            self.ui.show_error_screen(f"Nie znaleziono produktu o kodzie: {barcode}")
    
    def handle_confirm_employee_scan(self, barcode):
        """Obsługuje drugie skanowanie identyfikatora pracownika (potwierdzające)."""
        barcode = barcode.replace("-", "_")
        print(f"DEBUG: handle_confirm_employee_scan() - {barcode}")
        
        # Pobierz informacje o pracowniku z bazy danych
        employee = db_connector.get_employee_by_identifier(barcode)
        
        if employee:
            # Walidacja zgodności identyfikatora
            if employee['identyfikator'] == self.ui.first_scan_employee_id:
                # Zamiast wyświetlać ekran potwierdzenia, od razu przetwarzamy pobranie
                self.handle_withdrawal_confirmation(self.ui.current_product, employee, self.ui.quantity)
            else:
                self.ui.show_error_screen("Identyfikator nie zgadza się z początkowym! Spróbuj ponownie.")
        else:
            self.ui.show_error_screen(f"Nie znaleziono pracownika o identyfikatorze: {barcode}")

    def handle_withdrawal_confirmation(self, product, employee, quantity):
        """Obsługuje potwierdzenie pobrania produktu."""
        print(f"DEBUG: handle_withdrawal_confirmation() - Produkt={product['kod']}, Pracownik={employee['identyfikator']}, Ilość={quantity}")
        
        try:
            # Przetwórz pobranie w bazie danych
            result = db_connector.process_withdrawal(product['kod'], employee['identyfikator'], quantity)
            
            if result['success']:
                # Dodajemy szczegóły produktu do komunikatu sukcesu
                success_message = f"{result['message']}\n\nPobrany produkt: {product['opis']}\nKod: {product['kod']}\nIlość: {quantity}"
                self.ui.show_success_screen(success_message)
                # USUNIĘTE: Nie resetujemy skanera tutaj - za wcześnie!
                print("DEBUG: Transakcja zakończona pomyślnie, oczekiwanie na koniec waiting state")
            else:
                self.ui.show_error_screen(result['message'])
                
        except Exception as e:
            print(f"DEBUG: Błąd podczas potwierdzania transakcji: {e}")
            self.ui.show_error_screen("Błąd podczas zapisywania transakcji")

    def reset_scanner_after_waiting(self):
        """Resetuje scanner PO zakończeniu okresu oczekiwania."""
        try:
            print("DEBUG: reset_scanner_after_waiting() wywołane")
            # Sprawdź obecny stan last_code przed resetowaniem
            if hasattr(self.scanner, 'last_code'):
                print(f"DEBUG: Obecny last_code przed resetem: '{self.scanner.last_code}'")
            
            # Sprawdź czy scanner ma metodę reset_last_code
            if hasattr(self.scanner, 'reset_last_code'):
                self.scanner.reset_last_code()
                print("DEBUG: Scanner zresetowany metodą reset_last_code()")
            else:
                # Fallback - resetuj bezpośrednio atrybut last_code
                if hasattr(self.scanner, 'last_code'):
                    old_code = self.scanner.last_code
                    self.scanner.last_code = None
                    print(f"DEBUG: last_code zmienione z '{old_code}' na None")
                    
            # Sprawdź stan po resetowaniu
            if hasattr(self.scanner, 'last_code'):
                print(f"DEBUG: last_code po resecie: '{self.scanner.last_code}'")
                
        except Exception as e:
            print(f"DEBUG: Błąd podczas resetowania skanera: {e}")
    
    def run(self):
        """Uruchamia główną pętlę aplikacji."""
        self.root.mainloop()
    
    def on_close(self):
        """Obsługuje zamknięcie okna aplikacji."""
        self.scanner.stop_scanning()
        self.root.destroy()
    
    def signal_handler(self, sig, frame):
        """Obsługuje sygnały systemowe (np. Ctrl+C)."""
        print("Otrzymano sygnał zamknięcia. Zamykanie aplikacji...")
        self.on_close()
        sys.exit(0)
    
    def check_if_product(self, barcode):
        """Sprawdza, czy zeskanowany kod jest kodem produktu."""
        print(f"DEBUG: check_if_product() - sprawdzanie '{barcode}'")
        product = db_connector.get_product_by_code(barcode)
        result = product is not None
        print(f"DEBUG: check_if_product() - wynik: {result}")
        return result

# Uruchomienie aplikacji
if __name__ == "__main__":
    app = MagazynekApp()
    app.run()
