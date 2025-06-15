[🇵🇱 Przeczytaj po polsku](README.md)


# Magazyn 360

A complete warehouse management system consisting of a terminal application (Raspberry Pi) and a web-based system (Django) for warehouse administration.

---

## 🏗️ System Architecture

### **🖥️ Warehouse Terminal Application (Raspberry Pi)**
- **Device:** Raspberry Pi 4 with touchscreen
- **Interface:** Python Tkinter in fullscreen mode
- **Scanning:** USB barcode scanners (evdev) + barcode support or mobile phone scanner
- **Purpose:** Terminal for employees retrieving products from the warehouse

### **🌐 Django Web System**
- **Backend:** Django REST Framework
- **Frontend:** Admin panel + HTML5 interface for mobile scanning
- **API:** REST endpoints with token-based authorization
- **Purpose:** Managing warehouse, products, and retrievals

### **📷 Product Image Server**
- **Server:** Apache/nginx on a dedicated device
- **Protocol:** HTTPS with self-signed certificate for local network
- **Structure:** `/wydruki/{product_code}.png` – automatic mapping of codes to files
- **Integration:** Automatic display of product images in the terminal interface
- When creating a new product, the web system uploads the image to the Apache server, converting it to .png and resizing to 400x400
- This allows users to see product images during handling

---

## 🔄 Warehouse Operation Flow

### **Workflow on Raspberry Pi Terminal:**
1. **Authorization:** Employee scans their ID
2. **Product selection:** Scanning product barcode
3. **Confirmation:** Employee re-scans their ID
4. **Registration:** System automatically logs the retrieval in Django database

### **Management via Web System:**
- Add/edit products and employees
- Real-time inventory tracking
- Retrieval history and reporting
- Mobile scanning via browser (HTML5)

---

## 📁 Project Structure

magazynek-3d-system/
├── raspberry-pi-terminal/        # Terminal app (Raspberry Pi)
│   ├── main.py                   # Main application logic
│   ├── ui_manager.py             # Tkinter GUI interface
│   ├── barcode_scanner.py        # USB scanner handler
│   ├── api_connector.py          # Django API communication
│   ├── logo.png                  # Logo
│   └── requirements.txt          # Python dependencies
│
├── django-backend/               # Web system (Django)
│   ├── wydruki_web_api/          # Main Django project
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── panel_wydrukow/           # Warehouse app
│   │   ├── models.py             # Products, employees, withdrawals
│   │   ├── views.py              # API and web views
│   │   ├── templates/
│   │   │   └── scan.html         # Mobile scanning page
│   │   └── static/               # CSS, JS, images
│   └── requirements.txt
│
├── media-server/                 # Image server 
│   ├── apache-config/            # Apache HTTPS config
│   └── wydruki/                  # Product images directory
│       ├── PROD_001.png
│       ├── FRAME_002.png
│       └── ...
│
├── README-PL.md                  # Polish documentation
├── README-EN.md                  # English documentation
└── .env.example                  # Environment template


---

## ⚙️ Terminal App Features

### **User Interface:**
- **Welcome screen** with step-by-step instructions
- **Automatic USB scanner detection** with device filtering
- **Display of product images** from media server
- **Two-step employee ID validation**
- **Error handling** with Polish-language messages
- **Reset application** with special code "00"

### **Technical Components:**
- `main.py` – orchestrates application and business logic
- `ui_manager.py` – GUI with status screens
- `barcode_scanner.py` – scanner handling with ASCII mapping
- `api_barcode_scanner.py` – scanner support in browser
- `api_connector.py` – REST API communication with caching

---

## 🌐 Django Web System

### **REST API Endpoints:**
- `POST /api/scan-barcode/` – Save scanned barcode from mobile
- `GET /api/product/<code>/` – Product info
- `GET /api/employee/<id>/` – Employee info
- `POST /api/terminal/pobranie/` – Register product retrieval
- `GET /api/dashboard/stats/` – System stats (healthcheck)

### **Authorization:**
All endpoints require header:
```
Authorization: Token <your_token>
```

### **Admin Panel:**
- Manage products
- View retrieval history with dates and quantities
- Inventory management (add, delete, edit)

---

## 📱 Mobile Scanning

System supports scanning through mobile browser:
- **URL:** `https://your-server:8000/scan/`
- **Technology:** HTML5 + ZXing-js
- **Support:** iOS Safari, Android Chrome
- **Features:** Camera selection, targeting overlay, error handling

---

## 📸 Screenshots

System includes the following screens:
- **Welcome screen** with usage instructions
- **Employee ID confirmation**
- **Product info** with image
- **Success screen** after confirmation
- **Error screen** with clear messages
  


Non-Commercial License


Permission is granted to use, copy, modify, and distribute this software for 
NON-COMMERCIAL purposes only, including:
- Educational use
- Research purposes  
- Personal projects
- Portfolio demonstration

Commercial use, including but not limited to:
- Use in commercial products or services
- Integration into commercial software
- Revenue-generating activities

is PROHIBITED without explicit written permission from the author.


