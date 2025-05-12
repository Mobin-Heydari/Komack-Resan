from django.db import models
from django.utils.text import slugify



class Province(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام")

    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="اسلاگ")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        verbose_name="استان"
    )

    name = models.CharField(max_length=100, verbose_name="نام")

    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="اسلاگ")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name




class RecipientAddress(models.Model):

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name="شهر"
    )

    Recipient = models.ForeignKey(
        "Users.User",
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name="خدمات گیرنده"
    )

    title = models.CharField(max_length=100, verbose_name="عنوان")

    address = models.CharField(max_length=200, verbose_name="آدرس")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ساخته شده")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آپدیت شده")


    class Meta:
        verbose_name = "آدرس مشتری"
        verbose_name_plural = "آدرس های مشتری ها"

    def __str__(self):
        return f"{self.title} - {self.address}"
    