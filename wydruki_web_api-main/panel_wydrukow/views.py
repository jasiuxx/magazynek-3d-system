from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q, F  # DODANO F
from django.utils import timezone
from datetime import datetime, time
from .models import Wydruki, Pobrania, Pracownicy
from django.contrib import messages
from PIL import Image
from .forms import WydrukForm
import os
from django.db.models import Case, When, Value, IntegerField
import ftplib
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import IntegrityError
import paramiko
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView


def lista_wydrukow(request):
    # Obsługa wyszukiwania
    search_query = request.GET.get('search', '')
    wydruki = Wydruki.objects.all()
    
    if search_query:
        wydruki = wydruki.filter(
            Q(kod__icontains=search_query) | 
            Q(opis__icontains=search_query)
        )
    
    # Sortowanie: produkty z niskim stanem na górze - UŻYWAMY F('niski_stan')
    wydruki = wydruki.annotate(
        priorytet=Case(
            When(ilosc__lt=F('niski_stan'), then=Value(1)),  # ZMIENIONE z 3 na F('niski_stan')
            default=Value(2),
            output_field=IntegerField()
        )
    ).order_by('priorytet', 'kod')
    
    context = {
        'wydruki': wydruki,
        'search_query': search_query,
        'settings': settings,
    }
    return render(request, 'panel_wydrukow/lista_wydrukow.html', context)

def temp_stock_view(request):
    wydruki = Wydruki.objects.all()
    context = {
        'wydruki': wydruki,
        'settings': settings,
    }
    return render(request, 'panel_wydrukow/temp_stock_view.html', context)

# Reszta funkcji bez zmian...
def process_product_image(zdjecie, kod_produktu):
    """
    Wspólna funkcja do przetwarzania zdjęć produktów.
    Skaluje do 400x400, obsługuje przezroczystość PNG i zapisuje jako PNG.
    """
    img = Image.open(zdjecie)

    # Obsługa przezroczystości dla PNG (jak w oryginalnym kodzie)
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGBA', img.size, (255, 255, 255, 255))
        background.paste(img, mask=img.split()[3])  # Używamy kanału alpha jako maski
        img = background

    # DODANE SKALOWANIE DO 400x400 Z ZACHOWANIEM PROPORCJI
    img.thumbnail((400, 400), Image.Resampling.LANCZOS)
    
    # Wyśrodkowanie na białym tle 400x400
    background_400 = Image.new('RGB', (400, 400), (255, 255, 255))
    
    # Wyśrodkuj przeskalowany obraz na białym tle
    x = (400 - img.width) // 2
    y = (400 - img.height) // 2
    background_400.paste(img, (x, y))

    # Tymczasowe zapisanie pliku (zawsze jako PNG jak w oryginalnym kodzie)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'temp'), exist_ok=True)
    temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp', f'{kod_produktu}.png')
    
    # Zapisz jako PNG z optymalizacją (jak w oryginalnym kodzie)
    background_400.save(temp_file_path, 'PNG', optimize=True)
    
    return temp_file_path

def dodaj_wydruk(request):
    if request.method == 'POST':
        form = WydrukForm(request.POST, request.FILES)
        if form.is_valid():
            wydruk = form.save()
            
            # Obsługa przesyłania zdjęcia na SFTP
            zdjecie = request.FILES.get('zdjecie')
            if zdjecie:
                try:
                    # Użyj wspólnej funkcji do przetwarzania
                    temp_file_path = process_product_image(zdjecie, wydruk.kod)
                    
                    # Połączenie SFTP i przesłanie pliku
                    import paramiko
                    try:
                        transport = paramiko.Transport((settings.SFTP_HOST, 22))
                        transport.connect(username=settings.SFTP_USER, password=settings.SFTP_PASSWORD)
                        sftp = paramiko.SFTPClient.from_transport(transport)
                        
                        # Nazwa pliku zawsze z rozszerzeniem .jpg
                        remote_path = f"{wydruk.kod}.png"
                        
                        # Obsługa katalogu zdalnego (opcjonalnie)
                        if hasattr(settings, 'SFTP_DIRECTORY') and settings.SFTP_DIRECTORY:
                            try:
                                try:
                                    sftp.stat(settings.SFTP_DIRECTORY)
                                except:
                                    sftp.mkdir(settings.SFTP_DIRECTORY)
                                remote_path = f"{settings.SFTP_DIRECTORY}/{remote_path}"
                            except Exception as e:
                                print(f"Błąd podczas obsługi katalogu: {str(e)}")
                        
                        sftp.put(temp_file_path, remote_path)
                        sftp.close()
                        transport.close()
                        
                        messages.success(request, f'Produkt "{wydruk.kod}" został dodany wraz ze zdjęciem (400x400)!')
                    except Exception as e:
                        # Plan awaryjny - zapis lokalny
                        local_path = f'wydruki/{wydruk.kod}.png'
                        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'wydruki'), exist_ok=True)
                        full_local_path = os.path.join(settings.MEDIA_ROOT, local_path)
                        
                        import shutil
                        shutil.copy(temp_file_path, full_local_path)
                        
                        messages.warning(request, f'Produkt został dodany, ale wystąpił błąd podczas przesyłania zdjęcia: {str(e)}. Zdjęcie zostało zapisane lokalnie.')
                    
                    # Usunięcie tymczasowego pliku
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                        
                except Exception as e:
                    messages.warning(request, f'Produkt został dodany, ale wystąpił błąd podczas przetwarzania zdjęcia: {str(e)}')
            else:
                messages.success(request, f'Produkt "{wydruk.kod}" został pomyślnie dodany!')
            
            return redirect('panel_wydrukow:lista_wydrukow')
    else:
        form = WydrukForm()
    
    return render(request, 'panel_wydrukow/formularz_wydruku.html', {
        'form': form,
        'title': 'Dodaj nowy produkt',
    })

def edytuj_wydruk(request, id):
    wydruk = get_object_or_404(Wydruki, id=id)
    
    # Zapamiętaj stary kod przed edycją
    stary_kod = wydruk.kod
    
    if request.method == 'POST':
        form = WydrukForm(request.POST, request.FILES, instance=wydruk)
        if form.is_valid():
            wydruk = form.save()
            
            # Sprawdź czy kod się zmienił
            kod_zmieniony = stary_kod != wydruk.kod
            
            # Obsługa przesyłania zdjęcia
            zdjecie = request.FILES.get('zdjecie')
            
            if zdjecie:
                # SCENARIUSZ 1: Nowe zdjęcie zostało przesłane
                try:
                    # Usuń stary plik jeśli kod się zmienił lub nie
                    if kod_zmieniony:
                        try:
                            usun_stary_plik_sftp(stary_kod)
                        except Exception as e:
                            print(f"Nie udało się usunąć starego pliku: {str(e)}")
                    else:
                        try:
                            usun_stary_plik_sftp(wydruk.kod)  # Usuń plik o tej samej nazwie
                        except Exception as e:
                            print(f"Nie udało się usunąć starego pliku: {str(e)}")
                    
                    # Przetwórz i zapisz nowe zdjęcie
                    temp_file_path = process_product_image(zdjecie, wydruk.kod)
                    
                    # Połączenie SFTP i przesłanie nowego pliku
                    import paramiko
                    try:
                        transport = paramiko.Transport((settings.SFTP_HOST, 22))
                        transport.connect(username=settings.SFTP_USER, password=settings.SFTP_PASSWORD)
                        sftp = paramiko.SFTPClient.from_transport(transport)
                        
                        # Nazwa nowego pliku
                        remote_path = f"{wydruk.kod}.png"
                        
                        # Obsługa katalogu zdalnego
                        if hasattr(settings, 'SFTP_DIRECTORY') and settings.SFTP_DIRECTORY:
                            try:
                                try:
                                    sftp.stat(settings.SFTP_DIRECTORY)
                                except:
                                    sftp.mkdir(settings.SFTP_DIRECTORY)
                                
                                remote_path = f"{settings.SFTP_DIRECTORY}/{remote_path}"
                            except Exception as e:
                                print(f"Błąd podczas obsługi katalogu: {str(e)}")
                        
                        sftp.put(temp_file_path, remote_path)
                        sftp.close()
                        transport.close()
                        
                        messages.success(request, f'Produkt "{wydruk.kod}" został zaktualizowany wraz z nowym zdjęciem (400x400)!')
                    except Exception as e:
                        # Plan awaryjny - zapis lokalny
                        local_path = f'wydruki/{wydruk.kod}.png'
                        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'wydruki'), exist_ok=True)
                        full_local_path = os.path.join(settings.MEDIA_ROOT, local_path)
                        
                        import shutil
                        shutil.copy(temp_file_path, full_local_path)
                        
                        messages.warning(request, f'Produkt został zaktualizowany, ale wystąpił błąd podczas przesyłania zdjęcia: {str(e)}. Zdjęcie zostało zapisane lokalnie.')
                    
                    # Usunięcie tymczasowego pliku
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                        
                except Exception as e:
                    messages.warning(request, f'Produkt został zaktualizowany, ale wystąpił błąd podczas przetwarzania zdjęcia: {str(e)}')
            
            elif kod_zmieniony:
                # SCENARIUSZ 2: Brak nowego zdjęcia ale kod się zmienił - przemianuj stary plik
                try:
                    przemianuj_plik_sftp(stary_kod, wydruk.kod)
                    messages.success(request, f'Produkt "{wydruk.kod}" został zaktualizowany. Nazwa pliku zdjęcia została zmieniona z "{stary_kod}.png" na "{wydruk.kod}.png".')
                except Exception as e:
                    messages.warning(request, f'Produkt został zaktualizowany, ale wystąpił błąd podczas zmiany nazwy pliku zdjęcia: {str(e)}. Stare zdjęcie może się nie wyświetlać.')
            else:
                # SCENARIUSZ 3: Brak nowego zdjęcia i kod się nie zmienił
                messages.success(request, f'Produkt "{wydruk.kod}" został zaktualizowany!')
            
            return redirect('panel_wydrukow:lista_wydrukow')
    else:
        form = WydrukForm(instance=wydruk)
    
    return render(request, 'panel_wydrukow/formularz_wydruku.html', {
        'form': form,
        'wydruk': wydruk,
        'title': f'Edytuj produkt: {wydruk.kod}',
        'is_edit': True,
        'settings': settings,
    })

# Funkcje pomocnicze do zarządzania plikami SFTP
def usun_stary_plik_sftp(kod_pliku):
    """Usuwa plik z serwera SFTP"""
    import paramiko
    
    transport = paramiko.Transport((settings.SFTP_HOST, 22))
    transport.connect(username=settings.SFTP_USER, password=settings.SFTP_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    try:
        # Ścieżka do starego pliku
        stary_remote_path = f"{kod_pliku}.png"
        
        if hasattr(settings, 'SFTP_DIRECTORY') and settings.SFTP_DIRECTORY:
            stary_remote_path = f"{settings.SFTP_DIRECTORY}/{stary_remote_path}"
        
        # Usuń plik
        sftp.remove(stary_remote_path)
        print(f"✓ Usunięto stary plik: {stary_remote_path}")
        
    except Exception as e:
        print(f"⚠ Nie udało się usunąć starego pliku {kod_pliku}.png: {str(e)}")
        # Nie rzucamy wyjątku - to nie jest krytyczny błąd
    finally:
        sftp.close()
        transport.close()

def przemianuj_plik_sftp(stary_kod, nowy_kod):
    """Przemianowuje plik na serwerze SFTP"""
    import paramiko
    
    transport = paramiko.Transport((settings.SFTP_HOST, 22))
    transport.connect(username=settings.SFTP_USER, password=settings.SFTP_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    try:
        # Ścieżki do plików
        stary_remote_path = f"{stary_kod}.png"
        nowy_remote_path = f"{nowy_kod}.png"
        
        if hasattr(settings, 'SFTP_DIRECTORY') and settings.SFTP_DIRECTORY:
            stary_remote_path = f"{settings.SFTP_DIRECTORY}/{stary_remote_path}"
            nowy_remote_path = f"{settings.SFTP_DIRECTORY}/{nowy_remote_path}"
        
        # Sprawdź czy stary plik istnieje
        try:
            sftp.stat(stary_remote_path)
            # Przemianuj plik
            sftp.rename(stary_remote_path, nowy_remote_path)
            print(f"✓ Przemianowano plik: {stary_remote_path} → {nowy_remote_path}")
        except IOError:
            print(f"⚠ Stary plik {stary_remote_path} nie istnieje - brak pliku do przemianowania")
            # To nie jest błąd - może nie było wcześniej zdjęcia
        
    except Exception as e:
        print(f"✗ Błąd podczas przemianowania pliku: {str(e)}")
        raise e  # Rzuć wyjątek, aby wywołujący kod mógł obsłużyć błąd
    finally:
        sftp.close()
        transport.close()


def historia_pobran(request):
    # Obsługa filtrowania
    wydruk_id = request.GET.get('wydruk', '')
    pracownik_id = request.GET.get('pracownik', '')
    
    pobrania = Pobrania.objects.all().order_by('-data_pobrania')
    
    if wydruk_id:
        pobrania = pobrania.filter(wydruk_id=wydruk_id)
    
    if pracownik_id:
        pobrania = pobrania.filter(identyfikator=pracownik_id)
    
    wydruki = Wydruki.objects.all()
    # Kluczowa zmiana: filtrujemy tylko pracowników z niepustym identyfikatorem
    pracownicy = Pracownicy.objects.filter(identyfikator__isnull=False).exclude(identyfikator='')
    
    context = {
        'pobrania': pobrania,
        'wydruki': wydruki,
        'pracownicy': pracownicy,
        'wydruk_id': wydruk_id,
        'pracownik_id': pracownik_id,
    }
    return render(request, 'panel_wydrukow/historia_pobran.html', context)

def dashboard(request):
    # Statystyki - aktualny stan magazynu
    wydruki = Wydruki.objects.all()
    
    # Najczęściej pobierane wydruki (top 5)
    popularne_wydruki = Pobrania.objects.values('wydruk__kod', 'wydruk__opis').annotate(
        total=Sum('ilosc')
    ).order_by('-total')[:5]
    
    # Ostatnie pobrania
    ostatnie_pobrania = Pobrania.objects.all().order_by('-data_pobrania')[:10]
    
    # Wydruki z niskim stanem - UŻYWAMY F('niski_stan')
    niski_stan_wydruki = Wydruki.objects.filter(ilosc__lt=F('niski_stan'))  # ZMIENIONE z 3 na F('niski_stan')
    niski_stan = niski_stan_wydruki.count()
    
    # Dzisiejsze pobrania
    today = timezone.now().date()
    today_start = datetime.combine(today, time.min)
    today_end = datetime.combine(today, time.max)

    dzisiejsze_pobrania = Pobrania.objects.filter(
        data_pobrania__range=(today_start, today_end)
    ).count()
    
    wszystkie_pobrania = Pobrania.objects.all().count()

    context = {
        'wydruki': wydruki,
        'popularne_wydruki': popularne_wydruki,
        'ostatnie_pobrania': ostatnie_pobrania,
        'niski_stan': niski_stan,
        'niski_stan_wydruki': niski_stan_wydruki,
        'wszystkie_wydruki': wydruki.count(),
        'dzisiejsze_pobrania': dzisiejsze_pobrania,
        'wszystkie_pobrania': wszystkie_pobrania,
    }
    return render(request, 'panel_wydrukow/dashboard.html', context)

def usun_wydruk(request, id):
    wydruk = get_object_or_404(Wydruki, id=id)
    
    if request.method == 'POST':
        try:
            # Sprawdź czy istnieją powiązane pobrania
            pobrania_count = Pobrania.objects.filter(wydruk=wydruk).count()
            
            if pobrania_count > 0:
                messages.error(request, 
                    f'Nie można usunąć produktu "{wydruk.kod}" - istnieją powiązane wpisy w historii pobrań ({pobrania_count} rekordów). '
                    f'Usuń najpierw wszystkie powiązane pobrania.')
                return redirect('panel_wydrukow:lista_wydrukow')
            
            # Jeśli nie ma powiązanych pobrań, można bezpiecznie usunąć
            kod = wydruk.kod  # Zapamiętujemy kod przed usunięciem
            wydruk.delete()
            messages.success(request, f'Produkt "{kod}" został pomyślnie usunięty!')
            
        except IntegrityError as e:
            # Dodatkowe zabezpieczenie w przypadku innych ograniczeń bazy danych
            if 'foreign key constraint fails' in str(e):
                messages.error(request, 
                    f'Nie można usunąć produktu "{wydruk.kod}" - istnieją powiązane dane w systemie. '
                    f'Usuń najpierw wszystkie powiązane rekordy.')
            else:
                messages.error(request, f'Błąd podczas usuwania produktu: {str(e)}')
        except Exception as e:
            # Obsługa innych nieoczekiwanych błędów
            messages.error(request, f'Wystąpił nieoczekiwany błąd podczas usuwania produktu: {str(e)}')
    else:
        messages.error(request, 'Niedozwolona metoda żądania!')
        
    return redirect('panel_wydrukow:lista_wydrukow')


@require_POST
def cofnij_pobranie(request, pobranie_id):
        pobranie = get_object_or_404(Pobrania, id=pobranie_id)
        wydruk = pobranie.wydruk

        # Zwiększ ilość woreczków w magazynie o ilość z pobrania
        wydruk.ilosc += pobranie.ilosc
        wydruk.save()
        
        # Usuń rekord pobrania
        pobranie.delete()
        messages.success(request, f'Cofnięto pobranie: {wydruk.kod} - {pobranie.ilosc} woreczków. Stan magazynu został przywrócony.')
        
        return redirect(request.META.get('HTTP_REFERER', 'panel_wydrukow:historia_pobran'))


class BarcodeScanPageView(TemplateView):
    template_name = "panel_wydrukow/scan.html"