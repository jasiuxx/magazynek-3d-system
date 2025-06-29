# api_connector.py - zastępuje db_connector.py
import requests
import json
from datetime import datetime
import time
import urllib3
import urllib.request
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000/api')
API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    raise ValueError("API_TOKEN nie jest ustawiony! Sprawdź plik .env")
# Kontekst SSL z wyłączoną weryfikacją
ssl_context = ssl._create_unverified_context()

class APIConnector:
    def __init__(self):
        self.session = requests.Session()
        
        self.session.headers.update({
            'Authorization': f'Token {API_TOKEN}',
            'Content-Type': 'application/json'
        })
        self.session.verify = False  # <-- DODAJ TO!
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        

        # Cache dla często używanych danych
        self._employee_cache = {}
        self._product_cache = {}
        self._cache_timeout = 300  # 5 minut

    def _make_request(self, method, endpoint, data=None, params=None, retries=1):
        """Wykonuje żądanie HTTP z retry logic."""
        url = f"{API_BASE_URL}{endpoint}"
        
        for attempt in range(retries):
            try:
                if method.upper() == 'GET':
                    response = self.session.get(url, params=params, timeout=10)
                elif method.upper() == 'POST':
                    response = self.session.post(url, data=json.dumps(data) if data else None, timeout=10)
                else:
                    raise ValueError(f"Nieobsługiwana metoda HTTP: {method}")
                
                response.raise_for_status()
                return response.json()
                
            except requests.RequestException as e:
                print(f"Błąd API (próba {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
    
    def get_product_by_code(self, code):
        """Pobiera informacje o produkcie na podstawie kodu kreskowego."""
        # Sprawdź cache
        cache_key = f"product_{code}"
        if cache_key in self._product_cache:
            cached_data, timestamp = self._product_cache[cache_key]
            if time.time() - timestamp < self._cache_timeout:
                return cached_data
        
        try:
            data = self._make_request('GET', f'/product/{code}/')
            # Zapisz w cache
            self._product_cache[cache_key] = (data, time.time())
            return data
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            print(f"Błąd podczas pobierania produktu: {e}")
            return None
    
    def get_employee_by_identifier(self, identifier):
        """Pobiera informacje o pracowniku na podstawie identyfikatora."""
        # Sprawdź cache
        cache_key = f"employee_{identifier}"
        if cache_key in self._employee_cache:
            cached_data, timestamp = self._employee_cache[cache_key]
            if time.time() - timestamp < self._cache_timeout:
                return cached_data
        
        try:
            data = self._make_request('GET', f'/employee/{identifier}/')
            # Zapisz w cache
            self._employee_cache[cache_key] = (data, time.time())
            return data
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            print(f"Błąd podczas pobierania pracownika: {e}")
            return None
    
    def update_product_quantity(self, product_id, quantity_change):
        """Aktualizuje ilość produktu w magazynie (przestarzałe - używaj process_withdrawal)."""
        print("UWAGA: update_product_quantity jest przestarzałe. Używaj process_withdrawal.")
        return False
    
    def register_withdrawal(self, product_id, employee_data, quantity):
        """Rejestruje pobranie produktu (przestarzałe - używaj process_withdrawal)."""
        print("UWAGA: register_withdrawal jest przestarzałe. Używaj process_withdrawal.")
        return None
    
    def process_withdrawal(self, product_code, employee_identifier, quantity=1):
        """Przetwarza całą operację pobrania produktu przez API."""
        try:
            data = {
                'product_code': product_code,
                'employee_identifier': employee_identifier,
                'quantity': quantity
            }
            
            result = self._make_request('POST', '/terminal/pobranie/', data=data)
            
            # Wyczyść cache dla zaktualizowanego produktu
            cache_key = f"product_{product_code}"
            if cache_key in self._product_cache:
                del self._product_cache[cache_key]
            
            return result
            
        except requests.HTTPError as e:
            error_data = e.response.json() if e.response.headers.get('content-type') == 'application/json' else {}
            return {
                "success": False, 
                "message": error_data.get('message', f'Błąd HTTP: {e.response.status_code}')
            }
        except Exception as e:
            return {
                "success": False, 
                "message": f"Błąd połączenia z serwerem: {str(e)}"
            }
    
    def clear_cache(self):
        """Czyści cache danych."""
        self._employee_cache.clear()
        self._product_cache.clear()
    
    def health_check(self):
        """Sprawdza dostępność API."""
        try:
            response = self._make_request('GET', '/dashboard/stats/')
            return True
        except Exception:
            return False

    def get_image(self, url):
        """Pobiera obraz z wyłączoną weryfikacją SSL."""
        try:
            req = urllib.request.Request(url)
            req.add_header('Authorization', f'Token {API_TOKEN}')
            with urllib.request.urlopen(req, context=ssl_context) as response:
                return response.read()
        except Exception as e:
            print(f"Błąd podczas pobierania obrazu: {e}")
            return None

# Funkcje kompatybilne z db_connector.py dla łatwiejszej migracji
_api_connector = APIConnector()

def get_product_by_code(code):
    """Kompatybilna funkcja - pobiera produkt po kodzie."""
    return _api_connector.get_product_by_code(code)

def get_employee_by_identifier(identifier):
    """Kompatybilna funkcja - pobiera pracownika po identyfikatorze."""
    return _api_connector.get_employee_by_identifier(identifier)

def update_product_quantity(product_id, quantity_change):
    """Kompatybilna funkcja - przestarzała."""
    return _api_connector.update_product_quantity(product_id, quantity_change)

def register_withdrawal(product_id, employee_data, quantity):
    """Kompatybilna funkcja - przestarzała."""
    return _api_connector.register_withdrawal(product_id, employee_data, quantity)

def process_withdrawal(product_code, employee_identifier, quantity=1):
    """Kompatybilna funkcja - przetwarza pobranie."""
    return _api_connector.process_withdrawal(product_code, employee_identifier, quantity)

def health_check():
    """Sprawdza dostępność API."""
    return _api_connector.health_check()
