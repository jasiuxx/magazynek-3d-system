import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def get_db_connection():
    """Tworzy i zwraca połączenie z bazą danych."""
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        database=DB_NAME
    )
    return connection

def get_product_by_code(code):
    """Pobiera informacje o produkcie na podstawie kodu kreskowego."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM wydruki WHERE kod = %s"
    cursor.execute(query, (code,))
    product = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return product

def get_employee_by_identifier(identifier):
    """Pobiera informacje o pracowniku na podstawie identyfikatora."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM pracownicy WHERE identyfikator = %s"
    cursor.execute(query, (identifier,))
    employee = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return employee

def update_product_quantity(product_id, quantity_change):
    """Aktualizuje ilość produktu w magazynie."""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = "UPDATE wydruki SET ilosc = ilosc - %s WHERE id = %s"
    cursor.execute(query, (quantity_change, product_id))
    connection.commit()
    
    success = cursor.rowcount > 0
    
    cursor.close()
    connection.close()
    
    return success

def register_withdrawal(product_id, employee_data, quantity):
    """Rejestruje pobranie produktu."""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = """
    INSERT INTO pobrania 
    (wydruk_id, identyfikator, imie_pracownika, nazwisko_pracownika, ilosc) 
    VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor.execute(query, (
        product_id, 
        employee_data['identyfikator'],
        employee_data['imie_pracownika'],
        employee_data['nazwisko_pracownika'],
        quantity
    ))
    
    connection.commit()
    withdrawal_id = cursor.lastrowid
    
    cursor.close()
    connection.close()
    
    return withdrawal_id

def process_withdrawal(product_code, employee_identifier, quantity=1):
    """Przetwarza całą operację pobrania produktu (logika biznesowa)."""
    # Pobierz informacje o produkcie
    product = get_product_by_code(product_code)
    if not product:
        return {"success": False, "message": "Produkt nie znaleziony"}
    
    # Sprawdź, czy pracownik istnieje
    employee = get_employee_by_identifier(employee_identifier)
    if not employee:
        return {"success": False, "message": "Pracownik nie znaleziony"}
    
    # Sprawdź, czy jest wystarczająca ilość produktu
    if product['ilosc'] < quantity:
        return {"success": False, "message": "Niewystarczająca ilość produktu"}
    
    # Zaktualizuj ilość produktu
    update_success = update_product_quantity(product['id'], quantity)
    if not update_success:
        return {"success": False, "message": "Błąd aktualizacji stanu magazynowego"}
    
    # Zarejestruj pobranie
    withdrawal_id = register_withdrawal(product['id'], employee, quantity)
    
    return {
        "success": True, 
        "message": "Pobranie zarejestrowane pomyślnie",
        "withdrawal_id": withdrawal_id,
        "product": product,
        "employee": employee,
        "quantity": quantity
    }


