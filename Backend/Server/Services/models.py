from django.db import models
from Companies.models import Company
from Industries.models import ServiceIndustry



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

