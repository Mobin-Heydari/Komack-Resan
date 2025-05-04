from django.db import models

class ServiceProviderProfile(models.Model):

    class GenderChoices(models.TextChoices):
        WOMEN = 'W', 'خانوم'
        MAN = 'M', 'آقا'

    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="provider_profile",
        verbose_name="کاربر"
    )
    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        verbose_name="جنسیت"
    )
    age = models.PositiveIntegerField(
        default=18,
        verbose_name="سن"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="بیوگرافی",
        help_text="توضیح مختصر درباره خودتان"
    )
    profile_picture = models.ImageField(
        upload_to='Profiles/profile_pics/providers/',
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )
    experience_years = models.PositiveIntegerField(
        default=0,
        verbose_name="سال‌های تجربه"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="در دسترس بودن"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "پروفایل خدمات دهنده"
        verbose_name_plural = "پروفایل خدمات دهندگان"

    def __str__(self):
        return f"{self.user.username} - پروفایل خدمات دهنده"


class ServiceRecipientProfile(models.Model):

    class GenderChoices(models.TextChoices):
        WOMEN = 'W', 'خانوم'
        MAN = 'M', 'آقا'

    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="recipient_profile",
        verbose_name="کاربر"
    )
    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        verbose_name="جنسیت"
    )
    age = models.PositiveIntegerField(
        default=18,
        verbose_name="سن"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="بیوگرافی",
        help_text="توضیح مختصر درباره خودتان"
    )
    profile_picture = models.ImageField(
        upload_to='Profiles/profile_pics/recipients/',
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "پروفایل خدمات گیرنده"
        verbose_name_plural = "پروفایل خدمات گیرندگان"

    def __str__(self):
        return f"{self.user.username} - پروفایل خدمات گیرنده"




class AdminProfile(models.Model):

    class GenderChoices(models.TextChoices):
        WOMEN = 'W', 'خانوم'
        MAN = 'M', 'آقا'

    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="admin_profile",
        verbose_name="کاربر"
    )
    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        verbose_name="جنسیت"
    )
    age = models.PositiveIntegerField(
        default=18,
        verbose_name="سن"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="بیوگرافی",
        help_text="توضیح مختصر درباره خودتان"
    )
    profile_picture = models.ImageField(
        upload_to='Profiles/profile_pics/admin/',
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "پروفایل ادمین"
        verbose_name_plural = "پروفایل ادمین ها"

    def __str__(self):
        return f"{self.user.username} - پروفایل ادمین"
    


class SupportProfile(models.Model):

    class GenderChoices(models.TextChoices):
        WOMEN = 'W', 'خانوم'
        MAN = 'M', 'آقا'

    user = models.OneToOneField(
        "Users.User",
        on_delete=models.CASCADE,
        related_name="support_profile",
        verbose_name="کاربر"
    )
    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        verbose_name="جنسیت"
    )
    age = models.PositiveIntegerField(
        default=18,
        verbose_name="سن"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="بیوگرافی",
        help_text="توضیح مختصر درباره خودتان"
    )
    profile_picture = models.ImageField(
        upload_to='Profiles/profile_pics/support/',
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "پروفایل پشتیبان"
        verbose_name_plural = "پروفایل پشتیبان ها"

    def __str__(self):
        return f"{self.user.username} - پروفایل پشتیبان"