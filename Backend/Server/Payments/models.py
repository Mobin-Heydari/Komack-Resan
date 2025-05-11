import uuid
from django.db import models
from Invoices.models import Invoice

class PaymentInvoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'PE', 'در انتظار پرداخت'
        SUCCESS = 'SU', 'موفق'
        FAILED = 'FA', 'ناموفق'

    invoice = models.OneToOneField(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payment_invoice',
        verbose_name='فاکتور پرداخت'
    )

    amount = models.BigIntegerField(verbose_name='مبلغ پرداختی')

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='شناسه تراکنش'
    )

    payment_status = models.CharField(
        max_length=3,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING,
        verbose_name='وضعیت پرداخت'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پرداخت')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    def __str__(self):
        return f"Payment for Invoice #{self.invoice.id} - {self.get_payment_status_display()}"

    def mark_successful(self):
        """
        When a payment is confirmed (e.g., via a gateway callback),
        mark the payment and update the corresponding invoice.
        """
        self.payment_status = self.PaymentStatusChoices.SUCCESS
        self.save()
        # When payment succeeds, update the invoice’s is_paid flag.
        self.invoice.is_paid = True
        self.invoice.save()
