import threading
import time
import requests
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()

# Wyłącz ostrzeżenia o niezweryfikowanych certyfikatach
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class APIBarcodeScanner:
    def __init__(self, api_url=os.getenv('API_BASE_URL')):
        self.api_url = api_url
        self.callback = None
        self.is_running = False
        self.thread = None
        self.last_code = None
        self.session = requests.Session()
        self.session.verify = False  # Wyłącz weryfikację SSL
        self.session.headers.update({
            'Authorization': os.getenv('API_TOKEN'),
            'Content-Type': 'application/json'
        })

    def register_callback(self, callback):
        self.callback = callback

    def start_scanning(self):
        if self.is_running:
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._scan_loop, daemon=True)
        self.thread.start()

    def stop_scanning(self):
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def _scan_loop(self):
        while self.is_running:
            try:
                resp = self.session.get(self.api_url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    code = data.get("barcode")
                    if code and code != self.last_code:
                        self.last_code = code
                        if self.callback:
                            self.callback(code)
                time.sleep(1)
            except Exception as e:
                print(f"Błąd APIBarcodeScanner: {e}")
                time.sleep(2)



    def clear_api(self):
            """Czyści API i resetuje ostatni kod."""
            try:
                # Wyczyść API
                resp = self.session.delete(self.api_url, timeout=5)
                if resp.status_code == 200:
                    print("API wyczyszczone pomyślnie")
                
                # Resetuj lokalny cache
                self.last_code = None
                print("last_code zresetowane")
                
            except Exception as e:
                print(f"Błąd czyszczenia API: {e}")


    def reset_last_code(self):
        """Resetuje ostatni zeskanowany kod."""
        self.last_code = None
        print("APIBarcodeScanner: last_code zresetowane")
