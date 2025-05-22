from django.db import models

from Users.models import User
from OneTimePasswords.models import OneTimePassword


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
        verbose_name_plural = "رمز های یکبار مصرف ثبت نام کاربر"

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