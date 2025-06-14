#!/bin/bash

# Skrypt automatycznego wdrażania aplikacji Django do Docker z menu
# Autor: System magazynu wydruków 3D
# Data: $(date)

# Kolory dla komunikatów
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Konfiguracja
CONTAINER_NAME="django_app"
IMAGE_NAME="wydruki_web"
PORT="8001:8001"

# Funkcja pełnego wdrożenia
full_deploy() {
    echo -e "${GREEN}=== PEŁNE WDROŻENIE APLIKACJI ===${NC}"
    echo -e "${YELLOW}Rozpoczynam pełne wdrożenie kontenera...${NC}"

    # Krok 1: Zatrzymanie istniejącego kontenera
    echo -e "${YELLOW}Krok 1: Zatrzymywanie kontenera ${CONTAINER_NAME}...${NC}"
    if sudo docker ps -q -f name=${CONTAINER_NAME} | grep -q .; then
        sudo docker stop ${CONTAINER_NAME}
        echo -e "${GREEN}✓ Kontener zatrzymany${NC}"
    else
        echo -e "${YELLOW}⚠ Kontener nie był uruchomiony${NC}"
    fi

    # Krok 2: Usunięcie istniejącego kontenera
    echo -e "${YELLOW}Krok 2: Usuwanie kontenera ${CONTAINER_NAME}...${NC}"
    if sudo docker ps -a -q -f name=${CONTAINER_NAME} | grep -q .; then
        sudo docker rm ${CONTAINER_NAME}
        echo -e "${GREEN}✓ Kontener usunięty${NC}"
    else
        echo -e "${YELLOW}⚠ Kontener nie istniał${NC}"
    fi

    # Krok 3: Budowanie nowego obrazu
    echo -e "${YELLOW}Krok 3: Budowanie nowego obrazu ${IMAGE_NAME}...${NC}"
    if sudo docker build -t ${IMAGE_NAME} .; then
        echo -e "${GREEN}✓ Obraz zbudowany pomyślnie${NC}"
    else
        echo -e "${RED}✗ Błąd podczas budowania obrazu${NC}"
        return 1
    fi

    # Krok 4: Uruchomienie nowego kontenera
    echo -e "${YELLOW}Krok 4: Uruchamianie nowego kontenera...${NC}"
    if sudo docker run -d --restart=always --name ${CONTAINER_NAME} -p ${PORT} ${IMAGE_NAME}; then
        echo -e "${GREEN}✓ Kontener uruchomiony pomyślnie${NC}"
    else
        echo -e "${RED}✗ Błąd podczas uruchamiania kontenera${NC}"
        return 1
    fi

    # Krok 5: Sprawdzenie statusu
    echo -e "${YELLOW}Krok 5: Sprawdzanie statusu...${NC}"
    sleep 3
    if sudo docker ps | grep -q ${CONTAINER_NAME}; then
        echo -e "${GREEN}✓ Kontener działa poprawnie${NC}"
        echo -e "${GREEN}✓ Aplikacja dostępna pod adresem: http://$(hostname -I | cut -d' ' -f1):8001${NC}"
    else
        echo -e "${RED}✗ Kontener nie działa${NC}"
        echo -e "${YELLOW}Sprawdzam logi...${NC}"
        sudo docker logs ${CONTAINER_NAME}
        return 1
    fi


    echo -e "${GREEN}=== WDROŻENIE ZAKOŃCZONE POMYŚLNIE ===${NC}"
}

# Funkcja menu
show_menu() {
    clear
    echo -e "${BLUE}=== MENU WDRAŻANIA APLIKACJI DJANGO ===${NC}"
    echo -e "${BLUE}Kontener: ${CONTAINER_NAME}${NC}"
    echo -e "${BLUE}Obraz: ${IMAGE_NAME}${NC}"
    echo -e "${BLUE}Port: ${PORT}${NC}"
    echo "1. Pełne wdrożenie (stop + build + run)"
    echo "2. Tylko przebuduj obraz"
    echo "3. Restart kontenera"
    echo "4. Pokaż logi"
    echo "5. Pokaż logi na żywo"
    echo "6. Status kontenera"
    echo "7. Zatrzymaj kontener"
    echo "8. Uruchom kontener"
    echo "9. Wyczyść nieużywane obrazy"
    echo "0. Wyjście"
    echo -e "${BLUE}=======================================${NC}"
}

# Główna pętla
while true; do
    show_menu
    read -p "Wybierz opcję (0-9): " choice
    
    case $choice in
        1) # Pełne wdrożenie
            echo -e "${YELLOW}Wykonuję pełne wdrożenie...${NC}"
            if full_deploy; then
                echo -e "${GREEN}Pełne wdrożenie zakończone pomyślnie!${NC}"
            else
                echo -e "${RED}Wystąpił błąd podczas wdrożenia!${NC}"
            fi
            ;;
        2) # Tylko rebuild
            echo -e "${YELLOW}Przebudowuję obraz...${NC}"
            if sudo docker build -t ${IMAGE_NAME} .; then
                echo -e "${GREEN}✓ Obraz przebudowany pomyślnie${NC}"
            else
                echo -e "${RED}✗ Błąd podczas budowania obrazu${NC}"
            fi
            ;;
        3) # Restart
            echo -e "${YELLOW}Restartuję kontener...${NC}"
            if sudo docker restart ${CONTAINER_NAME}; then
                echo -e "${GREEN}✓ Kontener zrestartowany${NC}"
            else
                echo -e "${RED}✗ Błąd podczas restartu kontenera${NC}"
            fi
            ;;
        4) # Logi
            echo -e "${YELLOW}Pokazuję ostatnie logi...${NC}"
            sudo docker logs --tail 50 ${CONTAINER_NAME}
            ;;
        5) # Logi na żywo
            echo -e "${YELLOW}Pokazuję logi na żywo (Ctrl+C aby wyjść)...${NC}"
            sudo docker logs -f ${CONTAINER_NAME}
            ;;
        6) # Status
            echo -e "${YELLOW}Status kontenera:${NC}"
            if sudo docker ps | grep -q ${CONTAINER_NAME}; then
                echo -e "${GREEN}✓ Kontener działa${NC}"
                sudo docker ps | grep ${CONTAINER_NAME}
                echo ""
                echo -e "${BLUE}Statystyki kontenera:${NC}"
                sudo docker stats ${CONTAINER_NAME} --no-stream
            else
                echo -e "${RED}✗ Kontener nie działa${NC}"
                echo "Lista wszystkich kontenerów:"
                sudo docker ps -a | grep ${CONTAINER_NAME}
            fi
            ;;
        7) # Zatrzymaj
            echo -e "${YELLOW}Zatrzymuję kontener...${NC}"
            if sudo docker stop ${CONTAINER_NAME}; then
                echo -e "${GREEN}✓ Kontener zatrzymany${NC}"
            else
                echo -e "${RED}✗ Błąd podczas zatrzymywania kontenera${NC}"
            fi
            ;;
        8) # Uruchom
            echo -e "${YELLOW}Uruchamiam kontener...${NC}"
            if sudo docker start ${CONTAINER_NAME}; then
                echo -e "${GREEN}✓ Kontener uruchomiony${NC}"
            else
                echo -e "${RED}✗ Błąd podczas uruchamiania kontenera${NC}"
                echo "Spróbuj opcji 1 (Pełne wdrożenie)"
            fi
            ;;
        9) # Wyczyść obrazy
            echo -e "${YELLOW}Czyszczę nieużywane obrazy...${NC}"
            sudo docker image prune -f
            echo -e "${GREEN}✓ Nieużywane obrazy usunięte${NC}"
            ;;
        0) # Wyjście
            echo -e "${GREEN}Do widzenia!${NC}"
            exit 0
            ;;
        *) 
            echo -e "${RED}Nieprawidłowy wybór! Wybierz opcję 0-9.${NC}"
            ;;
    esac
    echo
    read -p "Naciśnij Enter aby kontynuować..."
done
