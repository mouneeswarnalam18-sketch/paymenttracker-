from django.db import models

class Customer(models.Model):
    customer_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            start_month = 6
            start_year = 2026

            for i in range(36):
                month = ((start_month - 1 + i) % 12) + 1
                year = start_year + ((start_month - 1 + i) // 12)

                Payment.objects.create(
                    customer=self,
                    month=month,
                    year=year,
                    amount=3000,
                    status='Not Paid'
                )

    def __str__(self):
        return self.name


class Payment(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)

    month = models.IntegerField()
    year = models.IntegerField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=3000
    )

    status = models.CharField(
        max_length=10,
        choices=[
            ('Paid','Paid'),
            ('Not Paid','Not Paid')
        ],
        default='Not Paid'
    )

    paid_date = models.DateField(
        null=True,
        blank=True
    )

    paid_time = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('customer', 'month', 'year')

    def __str__(self):
        return f"{self.customer.customer_code} - {self.month}/{self.year} - {self.status}"