from django.db import models


class Materiau(models.Model):
    """Type de matière plastique (PET Bleu, HDPE, PP, ...)."""
    nom = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True, blank=True)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "Matière plastique"
        verbose_name_plural = "Matières plastiques"

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.nom.upper().replace(" ", "-")[:20]
        super().save(*args, **kwargs)
