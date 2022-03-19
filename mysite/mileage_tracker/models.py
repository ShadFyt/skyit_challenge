from django.db import models
from datetime import date
from django.utils.text import slugify


class Vehicle(models.Model):
    """blueprint for Vehicle table

    ATTR:
    {
        mileage: int = 12331
        manufacturer: str = Ford
        status: str = active
    }
    """

    status_options = [("active", "Active"), ("inoperative", "Inoperative")]

    unit: str = models.CharField(primary_key=True, max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    mileage: int = models.IntegerField(blank=False)
    manufacturer: str = models.CharField(max_length=100, blank=False)
    status: str = models.CharField(
        choices=status_options, default="active", max_length=12
    )

    class Meta:
        ordering = ["created"]

    def __str__(self) -> str:
        return f"Unit #: {self.unit}, Mileage: {self.mileage}, Manufacturer: {self.manufacturer}, Status: {self.status}"


class Miles(models.Model):
    """Blueprint for `Miles` table

    ATTR:
        {
            mileage: int = 12340,
            date_created: date = "2022-03-16",
            vehicle: Vehicle
        }


    """

    mileage: int = models.IntegerField(blank=False)
    date_created: date = models.DateField(default=date.today)
    vehicle = models.ForeignKey(Vehicle, related_name="miles", on_delete=models.CASCADE)
    difference = models.IntegerField(null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return f"Date: {self.date_created}, Mileage: {self.mileage}, Unit #: {self.vehicle}, Difference: {self.difference}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.date_created} {self.vehicle.unit}")
        return super().save(*args, **kwargs)

    @property
    def get_difference(self):
        return self.vehicle.mileage - self.mileage
