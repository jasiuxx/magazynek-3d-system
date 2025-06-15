[🇵🇱 Read in Polish](README.md)

# Warehouse 360

A complete warehouse management system consisting of a terminal application (Raspberry Pi) and a web-based system (Django) for warehouse administration.

---

## 🏗️ System Architecture

### **🖥️ Warehouse Terminal Application (Raspberry Pi)**
- **Device:** Raspberry Pi 4 with touchscreen  
- **Interface:** Python Tkinter in fullscreen mode  
- **Scanning:** USB barcode scanners (evdev) + built‑in barcode handling or mobile scanner on a phone  
- **Purpose:** Terminal for employees retrieving products from the warehouse  

### **🌐 Django Web System**
- **Backend:** Django REST Framework  
- **Frontend:** Admin panel + HTML5 mobile scanning interface  
- **API:** REST endpoints with token authentication  
- **Purpose:** Managing warehouse, products, and withdrawals  

### **📷 Product Image Server**
- **Server:** Apache/nginx on a dedicated device  
- **Protocol:** HTTPS with a self‑signed certificate for the local network  
- **Structure:** `/wydruki/{product_code}.png` – automatic mapping of codes to files  
- **Integration:** Automatic display of product images in the terminal interface  
- When creating a new product, the web system uploads the image to Apache, converts it to `.png` and resizes it to 400×400  
- Ensures product images are visible during handling  

---

## 🔄 Warehouse Operation Flow

### **Workflow on Raspberry Pi Terminal:**
1. **Authorization:** Employee scans their ID  
2. **Product Selection:** Scan the product’s barcode  
3. **Confirmation:** Employee re‑scans their ID  
4. **Recording:** System automatically logs the withdrawal in the Django database  

### **Management via the Web System:**
- Add/edit products and employees  
- Real‑time inventory tracking  
- Withdrawal history and reporting  
- Mobile scanning via browser (HTML5)  

---

## 📁 Project Structure

```text
magazynek-3d-system/
├── raspberry-pi-terminal/        # Terminal app (Raspberry Pi)
│   ├── main.py                   # Main application logic
│   ├── ui_manager.py             # Tkinter GUI interface
│   ├── barcode_scanner.py        # USB scanner handling
│   ├── api_connector.py          # Django REST API connector
│   ├── logo.png                  # Logo
│   └── requirements.txt          # Python dependencies
│
├── django-backend/               # Web system (Django)
│   ├── wydruki_web_api/          # Main Django project
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # URL configuration
│   │   └── wsgi.py               # WSGI entry point
│   ├── panel_wydrukow/           # Warehouse app
│   │   ├── models.py             # Models: products, employees, withdrawals
│   │   ├── views.py              # API and web views
│   │   ├── templates/            # HTML templates
│   │   │   └── scan.html         # Mobile scanning page
│   │   └── static/               # Static files (CSS, JS, images)
│   └── requirements.txt          # Python dependencies for Django
│
├── media-server/                 # Image server
│   ├── apache-config/            # Apache HTTPS configuration
│   └── wydruki/                  # Product images directory
│       ├── PROD_001.png          # Image for product PROD_001
│       ├── FRAME_002.png         # Image for product FRAME_002
│       └── ...                   # Other product images
│
├── README-PL.md                  # Documentation in Polish
├── README-EN.md                  # Documentation in English
└── .env.example                  # Environment variables template
```

---

## ⚙️ Terminal Application Features

### **User Interface:**
- **Welcome screen** with step‑by‑step instructions  
- **Automatic USB scanner detection** with device filtering  
- **Display of product images** from the image server  
- **Two‑step employee ID validation**  
- **Error handling** with messages in Polish  
- **Application reset** via special code "00"  

### **Technical Components:**
- `main.py` – orchestrates the application and business logic  
- `ui_manager.py` – graphical interface with status screens  
- `barcode_scanner.py` – scanner handling with ASCII code mapping  
- `api_barcode_scanner.py` – browser‑based scanner support  
- `api_connector.py` – REST API communication with caching  

---

## 🌐 Django Web System

### **REST API Endpoints:**
- `POST /api/scan-barcode/` – Save mobile‑scanned barcode  
- `GET /api/product/<code>/` – Product information  
- `GET /api/employee/<id>/` – Employee data  
- `POST /api/terminal/pobranie/` – Register product withdrawal  
- `GET /api/dashboard/stats/` – System health and statistics  

### **Authorization:**
All endpoints require the header:
```
Authorization: Token <your_token>
```

### **Admin Panel:**
- Manage products  
- View withdrawal history with dates and quantities  
- Inventory management (add, delete, edit)  

---

## 📱 Mobile Scanning

The system also supports mobile browser scanning:
- **URL:** `https://your-server:8000/scan/`  
- **Technology:** HTML5 + ZXing-js  
- **Supported:** iOS Safari, Android Chrome  
- **Features:** Camera selection, targeting overlay, error handling  

---

## 📸 Screenshots

The system includes these screens:
- **Welcome screen** with instructions  
- **Employee ID confirmation**  
- **Product scanning**  
- **Product information** with image  
- **Transaction confirmation** and success screen  
- **Error screens** with clear messages  

---

## 🚀 Future Development

Focus on enhancing the Django admin panel so warehouse managers can customize functionality. Aim to make Warehouse 360 as versatile as possible for client needs.

---

## 📄 License

### Non‑Commercial Use
Code is available for review for:
- Educational and research purposes  
- Showcasing programming skills  
- Technical solution analysis  

### Commercial Use
Commercial use requires written permission from the author.
