#!/usr/bin/env python3
import sys
import time
import socket
import tkinter as tk
from tkinter import ttk

class BarcodeSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Symulator Skanera Kodów Kreskowych")
        self.root.geometry("400x200")
        
        # Inicjalizacja gniazda
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(('localhost', 12345))
            print("Połączono z główną aplikacją")
        except ConnectionRefusedError:
            print("Nie można połączyć się z główną aplikacją!")
            print("Upewnij się, że główna aplikacja jest uruchomiona.")
            sys.exit(1)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Ramka główna
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Pole do wprowadzania kodu
        ttk.Label(main_frame, text="Wprowadź kod:").pack(pady=5)
        self.code_entry = ttk.Entry(main_frame, width=40)
        self.code_entry.pack(pady=5)
        self.code_entry.bind('<Return>', self.on_enter)
        
        # Przycisk skanowania
        ttk.Button(main_frame, text="Skanuj", command=self.scan_code).pack(pady=5)
        
        # Pole statusu
        self.status_label = ttk.Label(main_frame, text="Gotowy do skanowania")
        self.status_label.pack(pady=10)
        
        # Obsługa zamknięcia okna
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def scan_code(self):
        """Obsługuje skanowanie kodu."""
        code = self.code_entry.get().strip()
        if code:
            self.send_code(code)
            self.code_entry.delete(0, tk.END)
    
    def on_enter(self, event):
        """Obsługuje naciśnięcie Enter."""
        self.scan_code()
    
    def send_code(self, code):
        """Wysyła kod do głównej aplikacji."""
        try:
            self.socket.sendall(f"{code}\n".encode())
            self.status_label.config(text=f"Zeskanowano: {code}")
        except:
            self.status_label.config(text="Błąd wysyłania kodu!")
    
    def on_close(self):
        """Obsługuje zamknięcie okna."""
        self.socket.close()
        self.root.destroy()
    
    def run(self):
        """Uruchamia symulator."""
        self.root.mainloop()

if __name__ == "__main__":
    simulator = BarcodeSimulator()
    simulator.run() 