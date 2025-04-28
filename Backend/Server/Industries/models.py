from django.db import models
from django.utils.text import slugify


class IndustryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="اسلاگ دسته‌بندی")
    icon = models.ImageField(upload_to='Industry/categories-icon/', null=True, blank=True, verbose_name="آیکون")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام صنعت")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="اسلاگ صنعت")
    
    category = models.ForeignKey(
        IndustryCategory,
        on_delete=models.CASCADE,
        related_name="industries",
        verbose_name="دسته‌بندی"
    )

    icon = models.ImageField(upload_to='Industry/industries-icon/', null=True, blank=True, verbose_name="آیکون")

    class Meta:
        verbose_name = "صنعت"
        verbose_name_plural = "صنایع"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
