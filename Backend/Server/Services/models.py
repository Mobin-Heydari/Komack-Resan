from django.db import models
from Companies.models import Company, CompanyCard, CompanyAccountant, CompanyExpert, CompanyReceptionist
from Users.models import User
from Addresses.models import RecipientAddress
from Items.models import FirstItem, SecondItem

import uuid



class Service(models.Model):

    class ServiceType(models.TextChoices):
        IN_HOUSE_SERVICE = 'IHS', 'خدمات در منزل'
        IN_COMPANY_SERVICE = 'ICS', 'خدمات در شرکت'

    class ServiceStatusChoices(models.TextChoices):
        PENDING = 'PE', 'درحال بررسی'
        IN_PROGRESS = 'IP', 'درحال اجرا'
        FINISHED = 'FI', 'تمام شده'
        CANCELED = 'CA', 'کنسل شده'
        FAILED = 'FA', 'شکست خورده'
        REPORTED = 'RE', 'گزارش شده'
    

    id = models.UUIDField(verbose_name="آیدیه سرویس", primary_key=True, default=uuid.uuid4)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="service_company",
        verbose_name="شرکت"
    )
    
    receptionist = models.ForeignKey(
        CompanyReceptionist,
        verbose_name="منشی سرویس",
        on_delete=models.CASCADE,
        related_name="receptionist_services"
    )

    accountant = models.ForeignKey(
        CompanyAccountant,
        verbose_name="حسابدار",
        on_delete=models.CASCADE,
        related_name="accountant_services"
    )

    expert = models.ForeignKey(
        CompanyExpert,
        verbose_name="متخصص",
        on_delete=models.CASCADE,
        related_name="expert_services"
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

    first_item = models.ForeignKey(
        FirstItem,
        on_delete=models.SET_NULL,
        verbose_name="آیتم یک",
        related_name="first_item_services", 
        blank=True, null=True
    )

    second_item = models.ForeignKey(
        SecondItem,
        on_delete=models.SET_NULL,
        verbose_name="آیتم دو",
        related_name="second_item_services",
        blank=True, null=True
    )

    title = models.CharField(max_length=255, verbose_name="عنوان")

    phone = models.CharField(max_length=11, verbose_name="شماره تلفن")

    descriptions = models.TextField(verbose_name="توضیحات")

    image = models.FileField(upload_to="Services/image/")

    service_status = models.CharField(
        max_length=3,
        choices=ServiceStatusChoices.choices,
        default=ServiceStatusChoices.PENDING,
        verbose_name="وضعیت سرویس"
    )

    service_type = models.CharField(
        max_length=3,
        verbose_name="نوع خدمات",
        choices=ServiceType.choices
    )

    is_invoiced = models.BooleanField(default=False, verbose_name="به فاکتور اضافه شده")
    is_validated_by_receptionist = models.BooleanField(default=False, verbose_name="تایید شده توسط منشی")

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


class ServicePayment(models.Model):

    class PaymentStatusChoices(models.TextChoices):
        PAID = 'PA', 'پرداخت شده'
        UNPAID = 'UP', 'پرداخت نشده'
        FAILED = 'FA', 'ناموفق'

    class PaymentMethodChoices(models.TextChoices):
        CASH = 'CA', 'نقدی'
        TRANSACTION = 'TR', 'کارت به کارت'
    

    service = models.OneToOneField(
        Service,
        on_delete=models.CASCADE,
        verbose_name="سرویس",
        related_name="service_payment"
    )

    price = models.BigIntegerField(verbose_name="قیمت")

    company_card = models.ForeignKey(
        CompanyCard,
        on_delete=models.SET_NULL,
        related_name="service_company_card",
        verbose_name="کارت",
        null=True, blank=True
    )

    payment_status = models.CharField(
        max_length=3,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.UNPAID,
        verbose_name="وضعیت پرداخت"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethodChoices.choices,
        verbose_name="روش پرداخت",
        null=True, blank=True
    )

    transaction_screenshot = models.ImageField(
        upload_to='Services/transaction_screenshots/',
        verbose_name="تصویر فاکتور تراکنش",
        null=True, blank=True
    )

    paied_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ پرداخت")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")


    class Meta:
        verbose_name = "اطلاعات پرداخت سرویس"
        verbose_name_plural = "اطلاعات پرداخت سرویس ها"