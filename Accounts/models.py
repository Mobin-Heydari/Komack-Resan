from django.db import models

from OneTimePasswords.models import OneTimePassword
from Users.models import User




class ResetPasswordOneTimePassword(models.Model):
    
    otp = models.ForeignKey(
        OneTimePassword,
        on_delete=models.CASCADE,
        verbose_name="کد اعتبار سنجی",
        related_name="reset_password"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )

    phone = models.CharField(max_length=12, verbose_name="شماره تلفن")

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )


    class Meta:
        verbose_name = "کد اعتبار سنجی رمزعبور"
        verbose_name_plural = "کد های اعتبار سنجی رمزعبور"
        
    
    def __str__(self):
        return f'{self.otp.token}----{self.otp.code}'