from django.db import models
from django.db.models import Avg
from Companies.models import Company
from Industries.models import ServiceIndustry
from Users.models import User
from Addresses.models import RecipientAddress




class Service(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="service_company",
        verbose_name="شرکت"
    )
    service_industry = models.ForeignKey(
        ServiceIndustry,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="صنعت سرویس"
    )
    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = models.SlugField(max_length=255, verbose_name="اسلاگ")
    descriptions = models.TextField(verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "سرویس"
        verbose_name_plural = "سرویس‌ها"

    def __str__(self):
        return self.title

    @property
    def average_scores(self):
        """
        Aggregates the average scores (quality, behavior, time)
        from the associated service requests that have been scored.
        """
        aggregate = self.serivice_recepient.filter(score__isnull=False).aggregate(
            avg_quality=Avg('score__quality'),
            avg_behavior=Avg('score__behavior'),
            avg_time=Avg('score__time')
        )
        return aggregate

    @property
    def overall_score(self):
        """
        Computes an overall score from the average metrics.
        """
        scores = self.average_scores
        if scores['avg_quality'] is not None:
            overall = (scores['avg_quality'] + scores['avg_behavior'] + scores['avg_time']) / 3
            return overall
        return None


class RecepientServiceRequest(models.Model):
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
    
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="serivice_recepient",
        verbose_name="سرویس"
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
    started_at = models.DateTimeField(null=True, verbose_name="زمان شروع")
    finished_at = models.DateTimeField(null=True, verbose_name="زمان پایان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "درخواست سرویس"
        verbose_name_plural = "درخواست‌های سرویس"

    def __str__(self):
        return self.title

    @property
    def has_score(self):
        """
        Returns True if this request already has an associated score.
        """
        return hasattr(self, 'score')
