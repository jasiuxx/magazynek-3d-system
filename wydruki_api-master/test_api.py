# test_api.py - test połączenia z API
import requests
import json

API_BASE_URL = "http://ADES:8000/api"
API_TOKEN = "TOKEN"  # Wstaw prawdziwy token

headers = {
    'Authorization': f'Token {API_TOKEN}',
    'Content-Type': 'application/json'
}

def test_api_connection():
    """Test podstawowego połączenia z API."""
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard/stats/", headers=headers, timeout=5)
        response.raise_for_status()
        print("✓ Połączenie z API działa!")
        print(f"Dane: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Błąd połączenia z API: {e}")
        return False

def test_terminal_workflow():
    """Test przepływu operacji terminalowej."""
    # Test 1: Pobierz pracownika
    try:
        response = requests.get(f"{API_BASE_URL}/employee/janszczudlo/", headers=headers)
        if response.status_code == 404:
            print("⚠ Brak testowego pracownika 'terminal_user' - utwórz go w panelu Django")
        else:
            print("✓ Endpoint pracownika działa")
    except Exception as e:
        print(f"✗ Błąd endpoint pracownika: {e}")
    
    # Test 2: Pobierz produkt
    try:
        response = requests.get(f"{API_BASE_URL}/product/TEST_001/", headers=headers)
        if response.status_code == 404:
            print("⚠ Brak testowego produktu 'TEST_001' - utwórz go w panelu Django")
        else:
            print("✓ Endpoint produktu działa")
    except Exception as e:
        print(f"✗ Błąd endpoint produktu: {e}")

if __name__ == "__main__":
    print("=== Test API Magazynku ===")
    test_api_connection()
    test_terminal_workflow()
