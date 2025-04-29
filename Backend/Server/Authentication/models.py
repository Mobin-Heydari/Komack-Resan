from django.db import models
from django.utils import timezone


class OneTimePassword(models.Model):
    class OtpStatus(models.TextChoices):
        EXPIRED = 'EXP' 
        ACTIVE = 'ACT'

    status = models.CharField(
        max_length=3,
        choices=OtpStatus.choices,
        default=OtpStatus.ACTIVE
    )
    
    token = models.CharField(
        max_length=250,
        unique=True
    )
    
    code = models.CharField(max_length=6)
    
    expiration = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )

    class Meta:
        verbose_name = "رمز یکبار مصرف"

    def __str__(self):
        return f'{self.status}----{self.code}----{self.token}'

    def get_expiration(self):
        expiration = self.created_at + timezone.timedelta(minutes=2)
        self.expiration = expiration
        self.save()

    def status_validation(self):
        if self.expiration <= timezone.now():
            self.status = 'EXP'
            return self.status
        else:
            return self.status


class UserRegisterOTP(models.Model):
    otp = models.OneToOneField(
        OneTimePassword,
        on_delete=models.CASCADE,
        related_name="registration_otps"
    )

    username = models.CharField(max_length=40)

    email = models.EmailField()

    phone = models.CharField(max_length=11)

    password = models.CharField(max_length=128)

    full_name = models.CharField(max_length=255)

    password_conf = models.CharField(max_length=255)

    user_type = models.CharField(
        max_length=2,
        default="JS"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )

    class Meta:
        verbose_name = "رمز یکبار مصرف ثبت نام کاربر"

    def __str__(self):
        return f"ثبت نام برای {self.username} - {self.otp.token}"
