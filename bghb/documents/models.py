from django.db import models
from countries.models import Country  # Импортируем модель Country из приложения countries


class DocumentType(models.Model):
    code = models.CharField(max_length=50, verbose_name="Код документа")
    name = models.CharField(max_length=255, verbose_name="Название типа документа")
    category = models.CharField(max_length=255, verbose_name="Категория документа", blank=True, null=True)
    type = models.CharField(max_length=255, verbose_name="Тип документа", blank=True, null=True)
    first_issue_date = models.DateField(verbose_name="Дата первой выдачи", blank=True, null=True)
    valid = models.BooleanField(verbose_name="Действующий", default=True)
    legal_status = models.TextField(verbose_name="Юридический статус/основная цель", blank=True, null=True)
    length = models.FloatField(verbose_name="Длина документа", blank=True, null=True)
    width = models.FloatField(verbose_name="Ширина документа", blank=True, null=True)
    pages = models.IntegerField(verbose_name="Количество страниц", blank=True, null=True)
    validity_period = models.IntegerField(verbose_name="Срок действия", blank=True, null=True)
    renewable = models.BooleanField(verbose_name="Возможность продления", default=False)
    
    # Внешний ключ на страну, которая выдает документ
    issuing_country = models.ForeignKey(
        Country, 
        on_delete=models.CASCADE, 
        verbose_name="Государство, выдающее документ",
        related_name='document_types'
        )

    def __str__(self):
        return f'{self.code} - {self.issuing_country}'

    class Meta:
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"


class DocumentFeature(models.Model):
    document_type = models.ForeignKey(DocumentType,
                                      on_delete=models.CASCADE, 
                                      verbose_name="Тип документа",
                                      related_name="features"
                                      )
    feature_name = models.CharField(max_length=255, verbose_name="Название особенности")

    def __str__(self):
        return f"{self.document_type.name} - {self.feature_name}"

    class Meta:
        verbose_name = "Особенность документа"
        verbose_name_plural = "Особенности документов"


class FeatureDetail(models.Model):
    document_feature = models.ForeignKey(DocumentFeature, 
                                         on_delete=models.CASCADE, 
                                         verbose_name="Особенность", 
                                         related_name="details"
                                         )
    key = models.CharField(max_length=255, 
                           verbose_name="Ключ (например, материал, цвет)",
                           blank=True, 
                           null=True,
                           )
    value = models.CharField(max_length=255, 
                             verbose_name="Значение (например, пластик, красный)",
                             blank=True, 
                             null=True, 
                             )
    image = models.ImageField(upload_to='feature_detail_images/', 
                              verbose_name="Изображение", 
                              blank=True, 
                              null=True
                              )

    def __str__(self):
        return f"{self.document_feature.feature_name} - {self.key}: {self.value}"

    class Meta:
        verbose_name = "Деталь особенности"
        verbose_name_plural = "Детали особенностей"
