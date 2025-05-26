from django.db import models
from django.utils.text import slugify




class FirstItem(models.Model):

    name = models.CharField(max_length=255, verbose_name="نام", unique=True)
    slug = models.SlugField(max_length=255, verbose_name="اسلاگ", unique=True)

    icon = models.FileField(
        upload_to="Items/first/",
        verbose_name="آیکون",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "آیتم یک"
        verbose_name_plural = "آیتم های یک"


    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(FirstItem, self).save(*args, **kwargs)
    

class SecondItem(models.Model):

    name = models.CharField(max_length=255, verbose_name="نام", unique=True)
    slug = models.SlugField(max_length=255, verbose_name="اسلاگ", unique=True)

    icon = models.FileField(
        upload_to="Items/second/",
        verbose_name="آیکون",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "آیتم دو"
        verbose_name_plural = "آیتم های دو"


    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SecondItem, self).save(*args, **kwargs)
