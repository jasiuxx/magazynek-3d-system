#!/usr/bin/env python3
from pynput import keyboard
import threading
import time

class BarcodeScanner:
    def __init__(self, device_name=None):
        """Inicjalizacja skanera kodów kreskowych.
        
        Args:
            device_name (str, optional): Nazwa urządzenia skanera (nieużywane w wersji macOS).
        """
        self.device_name = device_name
        self.callback = None
        self.is_running = False
        self.thread = None
        self.current_barcode = ""
        self.last_key_time = 0
        self.keyboard_listener = None
        
    def initialize(self):
        """Inicjalizuje skaner kodów kreskowych."""
        try:
            self.keyboard_listener = keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            return True
        except Exception as e:
            print(f"Błąd podczas inicjalizacji skanera: {e}")
            return False
    
    def register_callback(self, callback):
        """Rejestruje funkcję zwrotną wywoływaną po zeskanowaniu kodu.
        
        Args:
            callback (function): Funkcja przyjmująca jeden argument (zeskanowany kod).
        """
        self.callback = callback
    
    def start_scanning(self):
        """Rozpoczyna nasłuchiwanie na kody kreskowe."""
        if self.is_running:
            return
        
        if not self.keyboard_listener:
            if not self.initialize():
                return
        
        self.is_running = True
        self.keyboard_listener.start()
        print("Rozpoczęto skanowanie kodów kreskowych.")
    
    def stop_scanning(self):
        """Zatrzymuje nasłuchiwanie na kody kreskowe."""
        self.is_running = False
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        print("Zatrzymano skanowanie kodów kreskowych.")

    def _clean_barcode_format(self, barcode):
        """Konwertuje kody kreskowe do odpowiedniego formatu."""
        return barcode.replace("-", "_")
    
    def _on_key_press(self, key):
        """Obsługuje naciśnięcie klawisza."""
        if not self.is_running:
            return
        
        current_time = time.time()
        
        # Jeśli minęło więcej niż 0.1s od ostatniego klawisza, resetujemy kod
        if current_time - self.last_key_time > 0.1:
            self.current_barcode = ""
        
        self.last_key_time = current_time
        
        try:
            # Obsługa znaków ASCII
            if hasattr(key, 'char'):
                if key.char == '\r' or key.char == '\n':  # Enter
                    if self.current_barcode and self.callback:
                        cleaned_barcode = self._clean_barcode_format(self.current_barcode)
                        if cleaned_barcode.strip():
                            self.callback(cleaned_barcode)
                    self.current_barcode = ""
                else:
                    self.current_barcode += key.char
        except AttributeError:
            pass  # Ignoruj specjalne klawisze
    
    def _on_key_release(self, key):
        """Obsługuje zwolnienie klawisza."""
        pass  # Nie potrzebujemy obsługi zwolnienia klawisza

# Przykład użycia
if __name__ == "__main__":
    def on_barcode_scanned(barcode):
        print(f"Zeskanowany kod: {barcode}")
    
    scanner = BarcodeScanner()
    if scanner.initialize():
        scanner.register_callback(on_barcode_scanned)
        scanner.start_scanning()
        
        try:
            # Utrzymuj program działający
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Przerwano przez użytkownika.")
        finally:
            scanner.stop_scanning()
