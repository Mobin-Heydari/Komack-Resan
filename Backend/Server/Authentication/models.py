from django.db import models
from django.utils import timezone

from Users.models import User

import uuid


class OneTimePassword(models.Model):
    class OtpStatus(models.TextChoices):
        EXPIRED = 'EXP' 
        ACTIVE = 'ACT'
        USED = 'USE'

    status = models.CharField(
        max_length=3,
        choices=OtpStatus.choices,
        default=OtpStatus.ACTIVE
    )
    
    token = models.UUIDField(verbose_name="توکن", primary_key=True, default=uuid.uuid4)
    
    code = models.CharField(max_length=6)
    
    expiration = models.DateTimeField(blank=True, null=True)

    is_used = models.BooleanField(default=False, verbose_name="استفاده شده؟")
    
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
        if self.is_used == True:
            self.status = 'USE'
        if self.expiration <= timezone.now():
            if not self.status == 'USE':
                self.status = 'EXP'
                return self.status
            else:
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

    user_type = models.CharField(max_length=3)
    
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
        return f"{self.username} - {self.otp.token} - {self.user_type}"



class UserLoginOTP(models.Model):

    otp = models.ForeignKey(
        OneTimePassword,
        on_delete=models.CASCADE,
        related_name="login_otps",
        verbose_name="کد یکبار مصرف"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )

    phone = models.CharField(
        max_length=12,
        verbose_name="شماره تلفن"
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
        verbose_name = "رمز یکبار مصرف ورود کاربر"
        verbose_name_plural = "رمزهای یکبار مصرف ورود کاربران"

    def __str__(self):
        return f"ورود برای {self.user.phone} - {self.otp.token}"