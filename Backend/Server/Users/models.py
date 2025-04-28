from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin



class IdCardInFormation(models.Model):
    class IdCardStatus(models.TextChoices):
        PENDING = 'P', 'درحال برسی'
        VERIFIED = 'V', 'تایید شده'
        REJECTED = 'R', 'رد شده'

    id_card_number = models.CharField(
        verbose_name="شماره ملی",
        max_length=13,
        blank=True,
        null=True
    )

    id_card = models.FileField(
        upload_to='Users/id_cards/',
        verbose_name="کارت ملی",
        help_text="بارگذاری تصویر/اسکن کارت ملی",
        blank=True,
        null=True
    )

    id_card_status = models.CharField(
        max_length=1,
        choices=IdCardStatus.choices,
        default=IdCardStatus.PENDING,
        verbose_name="وضعیت کارت ملی",
        help_text="وضعیت بررسی کارت ملی"
    )

    class Meta:
        verbose_name = "اطلاعات carteau ملی"

    def __str__(self):
        id_val = self.id_card_number if self.id_card_number else "No ID"
        return f"{id_val} - {self.get_id_card_status_display()}"



class User(AbstractBaseUser, PermissionsMixin):
    class UserTypes(models.TextChoices):
        SERVICEPROVIDER = "SP", "خدمات دهنده"
        SERVICERECIPIENT = "SC", "خدمات گیرنده"
        OWNER = "OW", "مالک"
        SUPPORT = "SU", "پشتیبان"
        ADMIN = "AD", "مدیر"

    class AccountStatus(models.TextChoices):
        ACTIVE = "ACT", "فعال"
        SUSPENDED = "SUS", "تعلیق شده"


    id_card_info = models.OneToOneField(
        IdCardInFormation,
        on_delete=models.SET_NULL,
        verbose_name="اطلاعات کارت ملی",
        related_name="id_card_info",
        null=True,
        blank=True
    )

    user_type = models.CharField(
        max_length=2, 
        choices=UserTypes.choices,
        verbose_name="نوع کاربر"
    )

    status = models.CharField(
        max_length=3, 
        choices=AccountStatus.choices, 
        default=AccountStatus.ACTIVE, 
        verbose_name="وضعیت حساب کاربری"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="ایمیل"
    )

    phone = models.CharField(
        unique=True,
        max_length=11,
        verbose_name="شماره تلفن"
    )

    username = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="نام کاربری"
    )

    full_name = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name="نام و نام خوانوادگی"
    )
    
    joined_date = models.DateField(
        auto_now_add=True,
        verbose_name="تاریخ عضویت"
    )

    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ آخرین به‌روزرسانی"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    is_admin = models.BooleanField(
        default=False,
        verbose_name="مدیر"
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username", "email", "full_name", "user_type"]

    class Meta:
        ordering = ['joined_date']
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin
