from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from Services.models import RecepientServiceRequest


class ServiceScore(models.Model):
    service_request = models.OneToOneField(
        RecepientServiceRequest,
        on_delete=models.CASCADE,
        related_name="score",
        verbose_name="درخواست سرویس"
    )
    quality = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="کیفیت"
    )
    behavior = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="رفتار"
    )
    time = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="سرعت"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت امتیاز")

    class Meta:
        verbose_name = "امتیاز سرویس"
        verbose_name_plural = "امتیازات سرویس"

    def __str__(self):
        return f"امتیاز برای {self.service_request}"
