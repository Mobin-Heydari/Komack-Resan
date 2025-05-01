from django.db import models

from Companies.models import Company
from Services.models import Service


class Invoice(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name="شرکت"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ صدور فاکتور")

    month = models.PositiveSmallIntegerField(verbose_name="ماه")

    year = models.PositiveSmallIntegerField(verbose_name="سال")

    total_amount = models.BigIntegerField(default=0, verbose_name="مبلغ کل")

    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده")
    
    def calculate_total(self):
        total = sum(item.amount for item in self.items.all())
        self.total_amount = total
        self.save()
    
    def __str__(self):
        return f"Invoice for {self.company.name}: {self.month}/{self.year}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="فاکتور مربوطه"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name="سرویس",
        related_name="service_invice_item",
    )

    amount = models.BigIntegerField(verbose_name="مبلغ کل")  # unit_price * quantity (if applicable)\

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت مورد")
    
    def save(self, *args, **kwargs):
        # In a simple scenario, one service request corresponds to one service usage.
        self.amount = self.service.company.industry.price_per_service  # Adjust if quantity or discounts apply.
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.service.title} for {self.invoice.company.name} - {self.amount}"