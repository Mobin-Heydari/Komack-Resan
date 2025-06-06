from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from Users.models import User
from Industries.models import Industry
from Addresses.models import City, Province
from Items.models import FirstItem, SecondItem




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

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        related_name="city_companies",
        verbose_name="شهر",
        blank=True, null=True
    )

    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        related_name="province_companies",
        verbose_name="استان",
        blank=True, null=True
    )

    address = models.TextField(verbose_name="آدرس", null=True, blank=True)

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


    class Meta:
        verbose_name = "شرکت"
        verbose_name_plural = "شرکت ها"


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
        verbose_name="جواز کسب",
        null=True, blank=True
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
        verbose_name_plural = "وضعیت شرکت ها"


    def __str__(self):
        return f"Validation Status for {self.company.name}"

    def mark_as_validated(self):
        self.overall_status = 'approved'
        self.validated_at = timezone.now()
        self.save()



class CompanyReceptionist(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="receptionists",
        verbose_name="شرکت"
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="receptionist_company",
        verbose_name="کارمند"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "منشی"
        verbose_name_plural = "منشی‌ها"
    
    def __str__(self):
        return self.employee.username


class CompanyAccountant(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="accountants",
        verbose_name="شرکت"
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accountant_company",
        verbose_name="کارمند"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "حسابدار"
        verbose_name_plural = "حسابداران"
    
    def __str__(self):
        return self.employee.username


class CompanyExpert(models.Model):
    class ExpertServiceType(models.TextChoices):
        IN_HOUSE = 'IH', 'In House Service'
        COMPANY = 'CP', 'Company Service'
        BOTH = 'BO', 'Both'

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="experts",
        verbose_name="شرکت"
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expert_company",
        verbose_name="کارمند"
    )
    service_type = models.CharField(
        max_length=2,
        choices=ExpertServiceType.choices,
        default=ExpertServiceType.COMPANY,
        verbose_name="نوع سرویس"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "متخصص"
        verbose_name_plural = "متخصصان"
    
    def __str__(self):
        return f"{self.employee.username} ({self.get_service_type_display()})"


class WorkDay(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = 'MO', 'دوشنبه'
        TUESDAY = 'TU', 'سه‌شنبه'
        WEDNESDAY = 'WE', 'چهارشنبه'
        THURSDAY = 'TH', 'پنج‌شنبه'
        FRIDAY = 'FR', 'جمعه'
        SATURDAY = 'SA', 'شنبه'
        SUNDAY = 'SU', 'یکشنبه'

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
    

class CompanyFirstItem(models.Model):
    first_item = models.ForeignKey(
        FirstItem,
        on_delete=models.CASCADE,
        related_name="company_first_item",
        verbose_name="آیتم"
    )

    compay = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="companies_first_item",
        verbose_name="شرکت"
    )

    class Meta:
        verbose_name = "آیتم اول شرکت"
        verbose_name_plural = "آیتم های اول شرکت"



class CompanySecondItem(models.Model):
    second_item = models.ForeignKey(
        SecondItem,
        on_delete=models.CASCADE,
        related_name="company_second_item",
        verbose_name="آیتم"
    )

    compay = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="companies_second_item",
        verbose_name="شرکت"
    )

    class Meta:
        verbose_name = "آیتم دوم شرکت"
        verbose_name_plural = "آیتم های دوم شرکت"



class CompanyCard(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="company_card",
        verbose_name="شرکت"
    )

    card_number = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'^\d{16}$',
                message="Card number must consist of exactly 16 digits.",
                code="invalid_card_number"
            )
        ],
        verbose_name="شماره کارت"
    )

    expiration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ انقضا"
    )

    card_holder_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="مالک"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        verbose_name = "کارت شرکت"
        verbose_name_plural = "کارت های شرکت ها"
    
    def __str__(self):
        return f"{self.company.name} کارته"