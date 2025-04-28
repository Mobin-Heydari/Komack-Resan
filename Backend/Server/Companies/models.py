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

    @property
    def service_scores(self):
        """
        Dynamically fetch associated scores from the scores app.
        """
        from Scores.models import ServiceScore  # local import to avoid circular dependency
        return ServiceScore.objects.filter(service_request__service__company=self)

    @property
    def average_scores(self):
        """
        Aggregate the average quality, behavior, and time scores
        from all the company’s service reviews.
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
        Calculate the overall score as the average of the three metrics.
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
        'Company',
        on_delete=models.CASCADE,
        related_name='validation_status',
        verbose_name="شرکت"
    )
    
    business_license = models.FileField(
        upload_to="Companies/Validations/",
        verbose_name="جواز کسب"
    )

    tax_certificate = models.FileField(
        upload_to="Companies/Validations/",
        verbose_name="گواهی مالیاتی"
    )

    safety_clearance = models.FileField(
        upload_to="Companies/Validations/",
        verbose_name="مجوز ایمنی"
    )

    compliance_certificate = models.FileField(
        upload_to="Companies/Validations/",
        verbose_name="گواهینامه انطباق"
    )

    business_license_status = models.BooleanField(
        default=False,
        verbose_name="جواز کسب"
    )

    tax_certificate_status = models.BooleanField(
        default=False,
        verbose_name="گواهی مالیاتی"
    )

    safety_clearance_status = models.BooleanField(
        default=False,
        verbose_name="مجوز ایمنی"
    )

    compliance_certificate_status = models.BooleanField(
        default=False,
        verbose_name="گواهینامه انطباق"
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