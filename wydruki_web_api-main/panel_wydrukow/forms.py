from django import forms
from django.core.exceptions import ValidationError
from .models import Wydruki

class WydrukForm(forms.ModelForm):
    zdjecie = forms.ImageField(
        required=False,
        label='Zdjęcie produktu',
        help_text='Zdjęcie zostanie nazwane kodem produktu i przesłane na serwer'
    )

    class Meta:
        model = Wydruki
        fields = ['kod', 'opis', 'ilosc', 'szt_w_wor', 'niski_stan']  # DODANE niski_stan
        labels = {
            'kod': 'Kod produktu',
            'opis': 'Opis produktu',
            'ilosc': 'Ilość pudełek',
            'szt_w_wor': 'Sztuk w pudełku',
            'niski_stan': 'Próg niskiego stanu',  # NOWA ETYKIETA
        }
        widgets = {
            'kod': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wprowadź kod produktu'}),
            'opis': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Wprowadź opis produktu', 'rows': 3}),
            'ilosc': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'szt_w_wor': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'niski_stan': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'np. 5'}),  # NOWY WIDGET
        }

    def clean_kod(self):
        kod = self.cleaned_data.get('kod')
        if not kod:
            return kod

        # Sprawdź czy istnieje wydruk o takim kodzie
        existing = Wydruki.objects.filter(kod=kod)

        # Jeśli to edycja, wykluczamy bieżący rekord z wyszukiwania
        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise ValidationError('Produkt o takim kodzie już istnieje. Wybierz inny kod.')

        return kod

    def clean_niski_stan(self):
        """Walidacja pola niski_stan"""
        niski_stan = self.cleaned_data.get('niski_stan')
        if niski_stan is not None and niski_stan < 1:
            raise ValidationError('Próg niskiego stanu musi być większy niż 0.')
        return niski_stan
