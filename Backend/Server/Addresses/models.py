from django.db import models



class RecipientAddress(models.Model):

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
    