from django.db import models
from django.utils import timezone
from Companies.models import Company
from Services.models import Service

import uuid



class Invoice(models.Model):

    class DeadlineStatusChoices(models.TextChoices):
        ACTIVE = 'AC', 'فعال'
        EXPIRED = 'EX', 'منقضی شده'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name="شرکت"
    )
    total_amount = models.BigIntegerField(default=0, verbose_name="مبلغ کل")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده")
    
    deadline = models.DateTimeField(verbose_name="مهلت پرداخت", null=True)
    
    deadline_status = models.CharField(
        max_length=2,
        choices=DeadlineStatusChoices.choices,
        default=DeadlineStatusChoices.ACTIVE,
        verbose_name="وضعیت مهلت"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ صدور قبض")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "قبض"
        verbose_name_plural = "قبض ها"
    
    def calculate_total(self):
        total = sum(item.amount for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])
    
    def update_deadline_status(self):
        """
        Compares the current time with the invoice deadline and updates the deadline_status.
        If the current time is past the deadline, sets status to EXPIRED; otherwise, ACTIVE.
        Returns the updated status.
        """
        now = timezone.now()
        new_status = (
            self.DeadlineStatusChoices.EXPIRED
            if now > self.deadline
            else self.DeadlineStatusChoices.ACTIVE
        )
        if new_status != self.deadline_status:
            self.deadline_status = new_status
            self.save(update_fields=['deadline_status'])
        return self.deadline_status

    @property
    def is_overdue(self):
        """Returns True if the current time is past the deadline."""
        return timezone.now() > self.deadline

    def __str__(self):
        return f"Invoice for {self.company.name} (Due: {self.deadline.strftime('%Y-%m-%d %H:%M')})"


class InvoiceItem(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="قبض مربوطه"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name="سرویس",
        related_name="service_invoice_item",
    )
    amount = models.BigIntegerField(verbose_name="مبلغ کل")  # unit_price * quantity (if applicable)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت مورد")

    class Meta:
        verbose_name = "آیتم قبض"
        verbose_name_plural = "آیتم‌های قبض"
    
    def save(self, *args, **kwargs):
        # In our simple scenario, one service corresponds to one invoice item.
        self.amount = self.service.company.industry.price_per_service
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.service.title} for {self.invoice.company.name} - {self.amount}"
