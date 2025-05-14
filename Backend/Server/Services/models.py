from django.db import models
from Companies.models import Company, CompanyEmployee
from Users.models import User
from Addresses.models import RecipientAddress



class Service(models.Model):

    class PaymentStatusChoices(models.TextChoices):
        PAID = 'PA', 'پرداخت شده'
        UNPAID = 'UP', 'پرداخت نشده'
        FAILED = 'FA', 'ناموفق'
    
    class ServiceStatusChoices(models.TextChoices):
        PENDING = 'PE', 'درحال بررسی'
        IN_PROGRESS = 'IP', 'درحال اجرا'
        FINISHED = 'FI', 'تمام شده'
        CANCELED = 'CA', 'کنسل شده'
        FAILED = 'FA', 'شکست خورده'
        REPORTED = 'RE', 'گزارش شده'

    class PaymentMethodChoices(models.TextChoices):
        CASH = 'CA', 'نقدی'
        TRANSACTION = 'TR', 'کارت به کارت'

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="service_company",
        verbose_name="شرکت"
    )
    
    service_provider = models.ForeignKey(
        User,
        verbose_name="سرویس دهنده",
        on_delete=models.CASCADE,
        related_name="service_owner"
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recepient_services",
        verbose_name="سرویس گیرنده"
    )

    recipient_address = models.ForeignKey(
        RecipientAddress,
        on_delete=models.CASCADE,
        related_name="service_addresses",
        verbose_name="آدرس"
    )

    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = models.SlugField(max_length=255, verbose_name="اسلاگ")
    descriptions = models.TextField(verbose_name="توضیحات")
    
    payment_status = models.CharField(
        max_length=3,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.UNPAID,
        verbose_name="وضعیت پرداخت"
    )

    service_status = models.CharField(
        max_length=3,
        choices=ServiceStatusChoices.choices,
        default=ServiceStatusChoices.PENDING,
        verbose_name="وضعیت سرویس"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethodChoices.choices,
        verbose_name="روش پرداخت",
        null=True, blank=True
    )

    transaction_screenshot = models.ImageField(
        upload_to='Services/transaction_screenshots/',
        null=True,
        blank=True,
        verbose_name="تصویر فاکتور تراکنش"
    )

    is_invoiced = models.BooleanField(
        default=False,
        verbose_name="به فاکتور اضافه شده"
    )

    started_at = models.DateTimeField(null=True, verbose_name="زمان شروع")
    finished_at = models.DateTimeField(null=True, verbose_name="زمان پایان")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "سرویس"
        verbose_name_plural = "سرویس‌ها"

    def __str__(self):
        return self.title

    @property
    def has_score(self):
        """
        Returns True if this service already has an associated score.
        """
        return hasattr(self, 'score')

    @property
    def overall_score(self):
        """
        Computes an overall score from the score details.
        Returns the average of quality, behavior, and time if a score exists.
        Otherwise, returns None.
        """
        if self.has_score:
            # Access the related score via the one-to-one reverse relation.
            score = self.score
            return (score.quality + score.behavior + score.time) / 3
        return None



class ServiceEmployee(models.Model):

    job_title = models.CharField(max_length=255, verbose_name="سمت کاری")

    recipient_service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="service_workers",
        verbose_name="سرویس درخواست شده"
    )

    employee = models.ForeignKey(
        CompanyEmployee,
        on_delete=models.CASCADE,
        related_name="service_company_worker",
        verbose_name="کارمند شرکت"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "کارمند سرویس"
        verbose_name_plural = "کارمندان سرویس‌ها"

    def __str__(self):
        return self.job_title
