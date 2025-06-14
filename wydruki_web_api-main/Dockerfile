# Wybierz oficjalny obraz Pythona
FROM python:3.11-slim

# Ustaw katalog roboczy
WORKDIR /app

# Zainstaluj wymagane pakiety systemowe dla mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Skopiuj pliki projektu
COPY . .

# Zainstaluj zale¿noœci
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Skopiuj statyczne pliki (opcjonalnie mo¿esz to robiæ przy starcie kontenera)
RUN python manage.py collectstatic --noinput

# Okreœl port (typowo 8001 dla Django dev server)
EXPOSE 8001

# Domyœlna komenda uruchamiaj¹ca serwer
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
