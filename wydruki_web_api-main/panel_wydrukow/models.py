from django.db import models

class Pracownicy(models.Model):
    pracownicy_id = models.AutoField(primary_key=True)
    imie_pracownika = models.CharField(max_length=30)
    nazwisko_pracownika = models.CharField(max_length=30)
    dzial = models.CharField(max_length=30)
    identyfikator = models.CharField(max_length=30, unique=True, null=True)

    class Meta:
        db_table = 'pracownicy'
        unique_together = (('imie_pracownika', 'nazwisko_pracownika'),)

    def __str__(self):
        return f"{self.imie_pracownika} {self.nazwisko_pracownika} ({self.identyfikator})"

class Wydruki(models.Model):
    id = models.AutoField(primary_key=True)
    kod = models.CharField(max_length=50, unique=True)
    opis = models.TextField(blank=True, null=True)
    ilosc = models.IntegerField(default=0)
    szt_w_wor = models.IntegerField(default=1)
    niski_stan = models.IntegerField(default=1, help_text='Próg niskiego stanu dla tego produktu')  # NOWE POLE

    class Meta:
        db_table = 'wydruki'

    def __str__(self):
        return f"{self.kod} - {self.opis}"

    @property
    def stan_calkowity(self):
        return self.ilosc * self.szt_w_wor
    
    @property
    def ma_niski_stan(self):
        """Sprawdza czy produkt ma niski stan"""
        return self.ilosc < self.niski_stan

class Pobrania(models.Model):
    id = models.AutoField(primary_key=True)
    wydruk = models.ForeignKey(Wydruki, models.DO_NOTHING)
    identyfikator = models.ForeignKey(Pracownicy, models.DO_NOTHING, db_column='identyfikator', to_field='identyfikator')
    imie_pracownika = models.CharField(max_length=30, null=True)
    nazwisko_pracownika = models.CharField(max_length=30, null=True)
    ilosc = models.IntegerField()
    data_pobrania = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pobrania'

    def __str__(self):
        return f"{self.wydruk.kod} - {self.ilosc} szt. ({self.data_pobrania})"
