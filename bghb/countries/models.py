from django.db import models

# Create your models here.
class Country(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Полное название страны")
    short_name = models.CharField(max_length=255, verbose_name="Краткое название страны")
    code_3 = models.CharField(max_length=3, verbose_name="Код страны из 3 букв")
    code_2 = models.CharField(max_length=2, verbose_name="Код страны из 2 букв")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class EntryRegime(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна")
    regime = models.TextField(verbose_name="Режим въезда в РФ", null=True, blank=True)
    regulatory_legal_acts = models.TextField(verbose_name="Нормативно-правовой акт", null=True, blank=True)
    note = models.TextField(verbose_name="Примечание", blank=True, null=True)

    def __str__(self):
        return f"{self.country.short_name} - {self.regime}"

    class Meta:
        verbose_name = "Режим въезда"
        verbose_name_plural = "Режимы въезда"
