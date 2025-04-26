from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from Users.models import User



class Company(models.Model):
    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="مدیرعامل"
    )

    name = models.CharField(
        max_length=255, 
        unique=True,
        verbose_name="نام شرکت"
    )
    slug = models.SlugField(
        max_length=255, 
        unique=True,
        blank=True,
        verbose_name="اسلاگ"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="توضیحات"
    )
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name="وبسایت"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="ایمیل"
    )
    phone_number = models.CharField(
        max_length=20, 
        blank=True,
        null=True,
        verbose_name="شماره تماس"
    )

    logo = models.ImageField(
        upload_to='company/logos/',
        blank=True,
        null=True,
        verbose_name="لوگو"
    )

    banner = models.ImageField(
        upload_to='company/banners/',
        blank=True,
        null=True,
        verbose_name="بنر"
    )

    intro_video = models.FileField(
        upload_to='company/videos/',
        blank=True,
        null=True,
        verbose_name="ویدئوی معرفی"
    )

    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="آدرس"
    )

    postal_code = models.CharField(
        max_length=20, 
        blank=True,
        null=True,
        verbose_name="کد پستی"
    )

    founded_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="تاریخ تأسیس"
    )
    number_of_employees = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="تعداد کارکنان"
    )

    linkedin = models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک LinkedIn"
    )
    twitter = models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک Twitter"
    )
    instagram = models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک Instagram"
    )


    is_validated = models.BooleanField(
        default=False,
        verbose_name="تایید شده توسط ادمین",
        help_text="در صورت True بودن، شرکت توسط ادمین تایید شده است."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # در صورتی که فیلد slug خالی باشد، از نام شرکت تولید می‌شود.
        if not self.slug:
            self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

