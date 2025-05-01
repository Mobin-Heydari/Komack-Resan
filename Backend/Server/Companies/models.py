from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from Users.models import User
from Industries.models import Industry



class Company(models.Model):

    class ServiceType(models.TextChoices):
        IN_HOUSE_SERVICE = 'IHS', 'خدمات در منزل'
        IN_COMPANY_SERVICE = 'ICS', 'خدمات در شرکت'
        BOTH = 'BOT', 'هر دو'


    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="مدیرعامل"
    )

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        verbose_name="صنعت"
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

    service_type = models.CharField(
        max_length=3,
        verbose_name="نوع خدمات",
        choices=ServiceType.choices,
        default=ServiceType.IN_COMPANY_SERVICE
    )

    is_validated = models.BooleanField(
        default=False,
        verbose_name="تایید شده توسط ادمین",
        help_text="در صورت True بودن، شرکت توسط ادمین تایید شده است."
    )

    is_off_season = models.BooleanField(
        default=False,
        verbose_name="فصل تعطیلات / غیر کاری"
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

    @property
    def service_scores(self):
        """
        دریافت امتیازات سرویس‌های مربوط به این شرکت 
        از طریق ارتباط یک به یک بین سرویس و امتیاز.
        """
        from Scores.models import ServiceScore  # Import local to avoid circular dependency.
        return ServiceScore.objects.filter(service__company=self)

    @property
    def average_scores(self):
        """
        میانگین امتیازات کیفیت، رفتار و سرعت بر روی تمامی سرویس‌های این شرکت.
        """
        aggregate = self.service_scores.aggregate(
            avg_quality=models.Avg('quality'),
            avg_behavior=models.Avg('behavior'),
            avg_time=models.Avg('time')
        )
        return aggregate

    @property
    def overall_score(self):
        """
        محاسبه امتیاز کلی به عنوان میانگین سه شاخص.
        """
        scores = self.average_scores
        if scores['avg_quality'] is not None:
            overall = (scores['avg_quality'] + scores['avg_behavior'] + scores['avg_time']) / 3
            return overall
        return None



class CompanyValidationStatus(models.Model):

    class ValidationStatus(models.TextChoices):
        PENDING = 'P', 'درانتظار'
        APPROVED = 'A', 'تایید شده'
        REJECTED = 'R', 'رد شده'


    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name='validation_status',
        verbose_name="شرکت"
    )
    
    business_license = models.FileField(
        upload_to="Companies/Validations/",
        verbose_name="جواز کسب"
    )

    business_license_status = models.BooleanField(
        default=False,
        verbose_name="جواز کسب"
    )

    overall_status = models.CharField(
        max_length=20,
        choices=ValidationStatus.choices,
        default='pending',
        verbose_name="وضعیت کلی"
    )

    validated_by = models.ForeignKey(
        'Users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_companies",
        verbose_name="تایید شده توسط",
        help_text="ادمینی که شرکت را تایید کرده است."
    )

    validated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ تایید",
        help_text="زمان تایید شرکت توسط ادمین."
    )

    validation_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="یادداشت‌های تایید"
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
        verbose_name = "وضعیت شرکت"
        verbose_name = "وضعیت شرکت ها"


    def __str__(self):
        return f"Validation Status for {self.company.name}"

    def mark_as_validated(self):
        self.overall_status = 'approved'
        self.validated_at = timezone.now()
        self.save()


class CompanyEmployee(models.Model):

    class EmployeePositionChoices(models.TextChoices):
        RECEPTIONIST = 'RE', 'منشی'
        ACCOUNTANT = 'AC', 'حسابدار'
        EXPERT = 'EX', 'متخصص'

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="شرکت"
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="employee_company",
        verbose_name="کارمند"
    )

    position = models.CharField(
        max_length=2,
        choices=EmployeePositionChoices.choices,
        verbose_name="موقعیت شغلی"
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
        verbose_name ="کارمند"
        verbose_name ="کارمند ها"
    

    def __str__(self):
        return self.employee.username
    


class WorkDay(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = 'monday', 'دوشنبه'
        TUESDAY = 'tuesday', 'سه‌شنبه'
        WEDNESDAY = 'wednesday', 'چهارشنبه'
        THURSDAY = 'thursday', 'پنج‌شنبه'
        FRIDAY = 'friday', 'جمعه'
        SATURDAY = 'saturday', 'شنبه'
        SUNDAY = 'sunday', 'یکشنبه'

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='workdays',
        verbose_name="شرکت مربوطه"
    )

    day_of_week = models.CharField(
        max_length=10,
        choices=DayOfWeek.choices,
        verbose_name="روز هفته"
    )

    open_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="زمان شروع"
    )

    close_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="زمان پایان"
    )

    is_closed = models.BooleanField(
        default=False,
        verbose_name="تعطیل بودن"
    )


    class Meta:
        unique_together = ('company', 'day_of_week')
        verbose_name = "روز کاری"
        verbose_name_plural = "روزهای کاری"
        # Optionally, add ordering for a natural week order if desired.
        # ordering = ['day_of_week']


    def clean(self):
        """
        Ensure consistency:
          - If the day is marked as closed, no open or close times should be set.
          - Otherwise, both open_time and close_time must be provided.
        """
        if self.is_closed:
            if self.open_time or self.close_time:
                raise ValidationError("برای روز تعطیل، زمان شروع و پایان باید خالی باشد.")
        else:
            if self.open_time is None or self.close_time is None:
                raise ValidationError("برای روز کاری، هر دو زمان شروع و پایان باید تعیین شوند.")
    

    @property
    def time_range(self):
        """
        Returns a formatted string displaying working hours, or 'Closed' if the company is off.
        """
        if self.is_closed:
            return "Closed"
        if self.open_time and self.close_time:
            return f"{self.open_time.strftime('%H:%M')} - {self.close_time.strftime('%H:%M')}"
        return "Not Set"


    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.time_range}"
