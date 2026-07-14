from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from matieres.models import Materiau
from partenaires.models import Client


class Vente(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    materiau = models.ForeignKey(Materiau, on_delete=models.PROTECT)
    quantite = models.DecimalField(max_digits=12, decimal_places=2)
    prix_unitaire = models.DecimalField("Prix de vente", max_digits=12, decimal_places=2)
    montant_total = models.DecimalField(max_digits=14, decimal_places=2, editable=False, default=0)
    date_vente = models.DateField()
    numero_bon = models.CharField("N° du bon", max_length=50, unique=True)
    numero_facture = models.CharField(max_length=30, unique=True, blank=True)
    photo_bon = models.ImageField("Photo du bon de pesée", upload_to="bons_vente/%Y/%m/", blank=True, null=True)
    observations = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="ventes_creees")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_vente", "-id"]
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"

    def __str__(self):
        return f"Vente {self.numero_facture} - {self.materiau} ({self.client})"

    def save(self, *args, **kwargs):
        self.montant_total = (self.quantite or 0) * (self.prix_unitaire or 0)
        if not self.numero_facture:
            from django.utils import timezone
            year = timezone.now().year
            last = Vente.objects.filter(numero_facture__startswith=f"FA-{year}-").order_by("-id").first()
            seq = 1
            if last and last.numero_facture:
                try:
                    seq = int(last.numero_facture.split("-")[-1]) + 1
                except ValueError:
                    seq = Vente.objects.filter(date_vente__year=year).count() + 1
            self.numero_facture = f"FA-{year}-{seq:04d}"
        super().save(*args, **kwargs)

    @property
    def montant_paye(self):
        total = Decimal("0")
        for p in self.paiements.all():
            total += p.montant_total
        return total

    @property
    def reste_a_recevoir(self):
        return self.montant_total - self.montant_paye

    @property
    def statut_paiement(self):
        if self.montant_paye <= 0:
            return "Non payé"
        if self.reste_a_recevoir <= Decimal("0.01"):
            return "Payé"
        return "En cours"

    @property
    def statut_paiement_css(self):
        return {"Non payé": "non-paye", "En cours": "en-cours", "Payé": "paye"}[self.statut_paiement]


class PaiementVente(models.Model):
    class Mode(models.TextChoices):
        ESPECES = "especes", _("Espèces")
        CHEQUE = "cheque", _("Chèque")
        MIXTE = "mixte", _("Mixte (Espèces + Chèque)")

    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name="paiements")
    mode = models.CharField(max_length=10, choices=Mode.choices)
    montant_especes = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    date_paiement = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_paiement", "-id"]

    def __str__(self):
        return f"Paiement de {self.montant_total} DH pour {self.vente.numero_facture}"

    @property
    def montant_cheques(self):
        return self.cheques.exclude(statut="annule").aggregate(total=models.Sum("montant"))["total"] or Decimal("0")

    @property
    def montant_total(self):
        return (self.montant_especes or Decimal("0")) + self.montant_cheques


class ChequeVente(models.Model):
    class Statut(models.TextChoices):
        ATTENTE = "attente", _("En attente")
        ENCAISSE = "encaisse", _("Encaissé")
        ANNULE = "annule", _("Annulé")

    paiement = models.ForeignKey(PaiementVente, on_delete=models.CASCADE, related_name="cheques")
    numero = models.CharField("N° chèque", max_length=50)
    banque = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=14, decimal_places=2)
    date_encaissement = models.DateField("Date d'encaissement prévue")
    photo = models.ImageField(upload_to="cheques_vente/%Y/%m/", blank=True, null=True)
    statut = models.CharField(max_length=10, choices=Statut.choices, default=Statut.ATTENTE)

    class Meta:
        ordering = ["date_encaissement"]

    def __str__(self):
        return f"Chèque {self.numero} - {self.montant} DH"
