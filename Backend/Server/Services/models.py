from django.db import models
from Companies.models import Company
from Industries.models import ServiceIndustry
from Users.models import User
from Addresses.models import RecipientAddress


class Service(models.Model):
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="service_compay",
        verbose_name="شرکت"
    )

    service_industry = models.ForeignKey(
        ServiceIndustry,
        on_delete=models.CASCADE,
        related_name="service",
        verbose_name="صنعت سرویس"
    )

    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = models.SlugField(max_length=255, verbose_name="اسلاگ")
    descriptions = models.TextField(verbose_name="توضحات")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ساخته شده")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آپدیت شده")

    class Meta:
        verbose_name = "سرویس"
        verbose_name_plural = "سرویس ها"
    
    def __str__(self):
        return self.title




class RecepientServiceRequest(models.Model):

    class PaymentStatusChoices(models.TextChoices):
        PAIED = 'PA', 'پرداخت شده'
        UNPAIED = 'UP', 'پرداخت نشده'
        FAILED = 'FA', 'ناموفق'
    
    class ServiceStatusChoices(models.TextChoices):
        PENDING = 'PE', 'درحال برسی'
        IN_PROGRASS = 'IP', 'درحال اجرا'
        FINISHED = 'FI', 'تمام شده'
        CANCLED = 'CA', 'کنسل شده'
        FAILED = 'FA', 'شکست خورده'
        REPORTED = 'RE', 'گذارش شده'
    

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
    descriptions = models.TextField(verbose_name="توضحات")

    status = models.CharField(
        max_length=3, 
        choices=ServiceStatusChoices.choices, 
        default=ServiceStatusChoices.PENDING, 
        verbose_name="وضعیت کلی"
    )

    status = models.CharField(
        max_length=3, 
        choices=PaymentStatusChoices.choices, 
        default=PaymentStatusChoices.UNPAIED, 
        verbose_name="وضعیت پرداخت"
    )

    started_at = models.DateTimeField(verbose_name="شروع شده", null=True)
    finished_at = models.DateTimeField(verbose_name="تمام شده", null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ساخته شده")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آپدیت شده")

    class Meta:
        verbose_name = "سرویس درخواست شده"
        verbose_name_plural = "سرویس های درخواست شده"
    
    def __str__(self):
        return self.title