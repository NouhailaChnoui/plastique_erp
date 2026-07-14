from decimal import Decimal
from django.db import models


class Client(models.Model):
    nom = models.CharField(max_length=150)
    telephone = models.CharField(max_length=30, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nom"]

    def __str__(self):
        return self.nom

    @property
    def ventes(self):
        return self.vente_set.all()

    @property
    def nombre_ventes(self):
        return self.ventes.count()

    @property
    def total_achete(self):
        return self.ventes.aggregate(total=models.Sum("montant_total"))["total"] or Decimal("0")

    @property
    def total_paye(self):
        total = Decimal("0")
        for vente in self.ventes.all():
            total += vente.montant_paye
        return total

    @property
    def montant_restant(self):
        return self.total_achete - self.total_paye


class Fournisseur(models.Model):
    nom = models.CharField(max_length=150)
    telephone = models.CharField(max_length=30, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nom"]

    def __str__(self):
        return self.nom

    @property
    def achats(self):
        return self.achat_set.all()

    @property
    def nombre_achats(self):
        return self.achats.count()

    @property
    def total_achete(self):
        return self.achats.aggregate(total=models.Sum("montant_total"))["total"] or Decimal("0")

    @property
    def total_paye(self):
        total = Decimal("0")
        for achat in self.achats.all():
            total += achat.montant_paye
        return total

    @property
    def reste_a_payer(self):
        return self.total_achete - self.total_paye
