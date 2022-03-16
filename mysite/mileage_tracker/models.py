from django.db import models


class Vehicle(models.Model):
    """blueprint for Vehicle table

    Args:
        mileage: int = 12331
        manufacturer: str = Ford
        status: str = active
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
