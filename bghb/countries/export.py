from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont  # Для подключения TTF-шрифтов
from django.http import HttpResponse
from .models import Country
from documents.models import DocumentType, DocumentFeature, FeatureDetail

# Регистрируем шрифт, поддерживающий кириллицу
pdfmetrics.registerFont(TTFont('Arial', 'ofont.ru_Arial.ttf'))  # Укажите путь к файлу шрифта

def export_country_to_pdf(country):
    # Создаем буфер для хранения PDF
    buffer = BytesIO()

    # Создаем PDF-документ
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Устанавливаем шрифт по умолчанию для всех стилей
    for style_name in ['Title', 'Heading1', 'Heading2', 'Heading3', 'Heading4', 'Heading5', 'Normal']:
        if style_name in styles:
            styles[style_name].fontName = 'Arial'

    # Содержимое PDF
    content = []

    # Заголовок
    title = Paragraph(f"Информация о стране: {country.full_name}", styles['Title'])
    content.append(title)

    # Данные о стране
    country_data = [
        ["Поле", "Значение"],
        ["Полное название", country.full_name],
        ["Краткое название", country.short_name],
        ["Код (2 буквы)", country.code_2],
        ["Код (3 буквы)", country.code_3],
    ]

    # Создаем таблицу для страны
    country_table = Table(country_data)
    country_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Arial'),  # Используем Arial
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    content.append(country_table)
    content.append(Spacer(1, 12))  # Добавляем отступ

    # Информация о документах страны
    documents = country.document_types.all()
    if documents:
        documents_title = Paragraph("Документы страны", styles['Heading2'])
        content.append(documents_title)

        for document in documents:
            # Заголовок документа
            document_title = Paragraph(f"Документ: {document.name} ({document.code})", styles['Heading3'])
            content.append(document_title)

            # Данные о документе
            document_data = [
                ["Поле", "Значение"],
                ["Категория", document.category],
                ["Тип", document.type],
                ["Дата первой выдачи", document.first_issue_date],
                ["Действующий", "Да" if document.valid else "Нет"],
                ["Юридический статус", document.legal_status],
                ["Размеры", f"{document.length} x {document.width} см"],
                ["Количество страниц", document.pages],
                ["Срок действия", document.validity_period],
                ["Возможность продления", "Да" if document.renewable else "Нет"],
            ]

            # Создаем таблицу для документа
            document_table = Table(document_data)
            document_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Arial'),  # Используем Arial
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            content.append(document_table)
            content.append(Spacer(1, 12))  # Добавляем отступ

            # Информация об особенностях документа
            features = document.features.all()
            if features:
                features_title = Paragraph("Особенности документа", styles['Heading4'])
                content.append(features_title)

                for feature in features:
                    # Заголовок особенности
                    feature_title = Paragraph(f"Особенность: {feature.feature_name}", styles['Heading5'])
                    content.append(feature_title)

                    # Данные о деталях особенности
                    details = feature.details.all()
                    if details:
                        details_data = [["Ключ", "Значение", "Изображение"]]
                        for detail in details:
                            details_data.append([
                                detail.key,
                                detail.value,
                                "Есть" if detail.image else "Нет",
                            ])

                        # Создаем таблицу для деталей
                        details_table = Table(details_data)
                        details_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Arial'),  # Используем Arial
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ]))

                        content.append(details_table)
                        content.append(Spacer(1, 12))  # Добавляем отступ

    # Генерация PDF
    pdf.build(content)

    # Получаем содержимое буфера
    buffer.seek(0)
    return buffer